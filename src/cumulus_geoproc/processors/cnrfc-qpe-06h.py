"""
# California Nevada River Forecast Center

## QPE 06 hour total precipitation
"""


import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import pyplugs
from osgeo import gdal

from cumulus_geoproc import logger, utils
from cumulus_geoproc.utils import cgdal

gdal.UseExceptions()


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

    try:
        # Source and Destination as Paths
        # take the source path as the destination unless defined.
        src_path = Path(src)
        if dst is None:
            dst_path = src_path.parent
        else:
            dst_path = Path(dst)

        # change the suffix
        filename_tif = src_path.with_suffix(".tif")
        if (
            len(src_path.suffixes) >= 2
        ):  # 2 or more suffixes assumes pattern like *.tar.gz, *.nc.gz, *.grb.gz, etc
            filename_tif = Path(src_path.stem).with_suffix(".tif")

        try:
            ds = gdal.Open("/vsigzip/" + src)
        except RuntimeError as err:
            logger.warning(err)
            logger.warning(f'gunzip "{src}" and use as source file')
            src_unzip = utils.decompress(src, str(dst_path))
            ds = gdal.Open(src_unzip)

        dataset_meta = gdal.Info(ds, format="json")
        bands = dataset_meta["bands"]

        for band in bands:
            band_num = band["band"]
            band_meta = band["metadata"][""]

            # validTimes is a str with {} and can be eval() to set()
            valid_times = eval(band_meta["validTimes"])
            t1, t2 = valid_times
            valid_datetime = datetime.fromtimestamp(t2).replace(tzinfo=timezone.utc)

            raster_band = ds.GetRasterBand(band_num)
            nodata = raster_band.GetNoDataValue()

            cgdal.gdal_translate_w_options(
                tif := str(dst_path / filename_tif),
                ds,
                bandList=[band_num],
                noData=nodata,
            )

            # validate COG
            if (validate := cgdal.validate_cog("-q", tif)) == 0:
                logger.debug(f"Validate COG = {validate}\t{tif} is a COG")

            outfile_list = [
                {
                    "filetype": acquirable,
                    "file": tif,
                    "datetime": valid_datetime.isoformat(),
                    "version": None,
                },
            ]

    except (RuntimeError, KeyError, Exception) as ex:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback_details = {
            "filename": os.path.basename(exc_traceback.tb_frame.f_code.co_filename),
            "line number": exc_traceback.tb_lineno,
            "method": exc_traceback.tb_frame.f_code.co_name,
            "type": exc_type.__name__,
            "message": exc_value,
        }
        for k, v in traceback_details.items():
            logger.error(f"{k}: {v}")

    finally:
        ds = None
    return outfile_list
