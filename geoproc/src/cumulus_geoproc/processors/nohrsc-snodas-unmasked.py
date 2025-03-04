"""
# NOHRSC SNODAS Unmasked
"""

import os
from datetime import datetime, timezone

import pyplugs
from cumulus_geoproc import logger, utils
from cumulus_geoproc.geoprocess import snodas
from cumulus_geoproc.geoprocess.snodas import metaparse
from cumulus_geoproc.utils import cgdal, file_extension
from osgeo import gdal

gdal.UseExceptions()

this = os.path.basename(__file__)


@pyplugs.register
def process(*, src: str, dst: str = None, acquirable: str = None):
    """
    # Grid processor

    __Requires keyword only arguments (*)__

    Parameters
    ----------
    src : str
        path to input file for processing
    dst : str, optional
        path to temporary directory
    acquirable: str, optional
        acquirable slug

    Returns
    -------
    List[dict]
    ```
    {
        "filetype": str,         Matching database acquirable
        "file": str,             Converted file
        "datetime": str,         Valid Time, ISO format with timezone
        "version": str           Reference Time (forecast), ISO format with timezone
    }
    ```
    """
    outfile_list = []

    paramater_codes = ["1034", "1036", "1038", "1044"]

    try:
        filename = os.path.basename(src)
        filename_dst = utils.file_extension(filename)

        # Take the source path as the destination unless defined.
        # User defined `dst` not programatically removed unless under
        # source's temporary directory.
        if dst is None:
            dst = os.path.dirname(src)

        # decompress the tar and gzip files in the tar
        decompressed_files = utils.decompress(src, dst, recursive=True)
        if not os.path.isdir(decompressed_files):
            raise Exception(f"Not a directory: {decompressed_files}")

        # generator for only the files ending with .txt
        txt_files = (f for f in os.listdir(decompressed_files) if f.endswith(".txt"))

        translate_to_tif = {}
        # create tif files for only the files needed
        for txt_file in txt_files:
            snodas_product_code = txt_file[8:12]
            if snodas_product_code in paramater_codes:
                fqpn = os.path.join(decompressed_files, txt_file)
                meta_ntuple = metaparse.to_namedtuple(fqpn)
                data_filename = meta_ntuple.data_file_pathname
                region = txt_file[:2]
                stop_date = datetime(
                    meta_ntuple.stop_year,
                    meta_ntuple.stop_month,
                    meta_ntuple.stop_day,
                    # Metadata value `Stop hour: 5` present in earlier SNODAS files results in incorrect timestamp if used directly as the timestamp for the data
                    # This has since been corrected in the SNODAS metadata .txt files. `Stop hour: 5` is no longer present in current files as of today (2022-08-08)
                    # Additional Information: https://github.com/USACE/cumulus/issues/264, https://github.com/USACE/cumulus/issues/244#issuecomment-1209465407
                    meta_ntuple.stop_hour if meta_ntuple.stop_year >= 2022 else 6,
                    meta_ntuple.stop_minute,
                    meta_ntuple.stop_second,
                    tzinfo=timezone.utc,
                )

                # FQPN to data file
                datafile_pathname = os.path.join(decompressed_files, data_filename)
                logger.debug(f"Data File Path: {datafile_pathname}")

                # write hdr so gdal can tranlate
                hdr_file = metaparse.write_hdr(
                    fqpn, meta_ntuple.number_of_columns, meta_ntuple.number_of_rows
                )
                # translate to tif
                if hdr_file is not None:
                    # set translate options
                    ds = gdal.Open(datafile_pathname)

                    cgdal.gdal_translate_w_options(
                        tif := file_extension(datafile_pathname, suffix=".tif"),
                        ds,
                        outputSRS=f"+proj=longlat +ellps={meta_ntuple.horizontal_datum} +datum={meta_ntuple.horizontal_datum} +no_defs",
                        noData=int(meta_ntuple.no_data_value),
                        outputBounds=[
                            meta_ntuple.minimum_x_axis_coordinate,
                            meta_ntuple.maximum_y_axis_coordinate,
                            meta_ntuple.maximum_x_axis_coordinate,
                            meta_ntuple.minimum_y_axis_coordinate,
                        ],
                    )

                    # validate COG
                    if (validate := cgdal.validate_cog("-q", tif)) == 0:
                        logger.debug(f"Validate COG = {validate}\t{tif} is a COG")

                    ds = None

                    # add tif dictionary to compute cold content
                    translate_to_tif[snodas_product_code] = {
                        "file": tif,
                        "filetype": snodas.product_code[snodas_product_code]["product"],
                        "datetime": stop_date.isoformat(),
                        "version": None,
                    }
                    logger.debug(f"Update Tif: {translate_to_tif[snodas_product_code]}")

        # cold content = swe * 2114 * snowtemp (degc) / 333000
        # id 2072
        if result := snodas.cold_content(translate_to_tif):
            translate_to_tif.update(result)
            logger.debug(f"Cold content product computed and dictionary updated")

        # convert snow melt to mm
        if result := snodas.snow_melt_mm(translate_to_tif):
            translate_to_tif.update(result)
            # remove snowmelt with unit meters and scale factor 100_000
            _ = translate_to_tif.pop("1044", None)
            logger.debug(
                f"Snow melt product conversion and original popped from dictionary"
            )

        outfile_list.extend(list(translate_to_tif.values()))

    except (RuntimeError, KeyError, Exception) as ex:
        logger.error(f"{type(ex).__name__}: {this}: {ex}")
    finally:
        ds = None

    return outfile_list
