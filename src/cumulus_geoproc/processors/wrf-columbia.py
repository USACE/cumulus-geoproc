"""
# Weather Research and Forecasting (WRF)

A next-generation mesoscale numerical weather prediction system designed for both atmospheric research and operational forecasting applications.

**details** [here](https://www.mmm.ucar.edu/weather-research-and-forecasting-model)

## WRF Columbia River Basin

**WRF Domain 3**
"""


import os
import sys
from datetime import timezone
from tempfile import TemporaryDirectory

import pyplugs
from cumulus_geoproc import logger
from cumulus_geoproc.utils import cgdal
from netCDF4 import Dataset, date2index, num2date
from osgeo import gdal


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

    src_dir = os.path.dirname(src)
    src_filename = os.path.basename(src)
    src_stem = os.path.splitext(src_filename)[0]

    wrf, basin, _, para = src_stem.split("-")
    product_slug = "-".join([wrf, basin, para])  # join back to be the product slug

    try:
        # extract the single grid from the source and create a temporary netCDF file
        with Dataset(src, "r") as ncsrc:
            nctime = ncsrc.variables["time"]
            for dt in num2date(
                nctime[:], nctime.units, only_use_cftime_datetimes=False
            ):
                dt_valid = dt.replace(tzinfo=timezone.utc)
                idx = date2index(dt, nctime)

                # context handling temp dir for extracting data to .nc
                with TemporaryDirectory(dir=dst) as tmpdir:
                    ncdst_path = os.path.join(tmpdir, para + ".nc")
                    # context handling writing to .nc file
                    with Dataset(ncdst_path, "w") as ncdst:
                        # Create dimensions
                        for name, dimension in ncsrc.dimensions.items():
                            dim_size = 1 if name == "time" else dimension.size
                            ncdst.createDimension(name, dim_size)
                        # Create variables, copy data, and set attributes
                        for name, variable in ncsrc.variables.items():
                            ncdst.createVariable(
                                name, variable.dtype, variable.dimensions
                            )
                            if name == "var" or name == "time" or name == "times":
                                ncdst.variables[name][:] = ncsrc.variables[name][idx]
                            else:
                                ncdst.variables[name][:] = ncsrc.variables[name][:]

                            ncdst.variables[name].setncatts(
                                ncsrc.variables[name].__dict__
                            )
                    # warp the extracted
                    gdal.Warp(
                        tiffile := os.path.join(
                            dst,
                            ".".join(
                                [
                                    product_slug,
                                    dt_valid.strftime("%Y%m%d%H"),
                                    "tif",
                                ]
                            ),
                        ),
                        f"NETCDF:{ncdst_path}:var",
                        format="COG",
                        srcSRS="EPSG:4326",
                        dstSRS="EPSG:4326",
                        resampleAlg="bilinear",
                        creationOptions=[
                            "COMPRESS=DEFLATE",
                            "PREDICTOR=2",
                        ],
                        geoloc=True,
                    )

                    # This GDAL Warp is essentially what would happen from
                    # the Cumulus packager before writing a record to DSS
                    # proj4_aea = "+proj=aea +lat_1=29.5 +lat_2=45.5 +lat_0=23 +lon_0=-96 +x_0=0 +y_0=0 +ellps=GRS80 +datum=NAD83 +units=m +no_defs"
                    # gdal.Warp(
                    #     another_tiffile := dst_dir.joinpath(
                    #         ".".join(
                    #             [
                    #                 product_slug,
                    #                 dt_valid.strftime("%Y%m%d%H"),
                    #                 "tiff",
                    #             ]
                    #         )
                    #     ).as_posix(),
                    #     tiffile,
                    #     format="COG",
                    #     outputBounds=[-2304000, 2034000, -804000, 3624000],
                    #     outputBoundsSRS=proj4_aea,
                    #     xRes=2000,
                    #     yRes=2000,
                    #     dstSRS=proj4_aea,
                    #     outputType=gdal.GDT_Float32,
                    #     resampleAlg="bilinear",
                    #     creationOptions=[
                    #         "COMPRESS=DEFLATE",
                    #         "PREDICTOR=2",
                    #     ],
                    #     dstNodata=-9999,
                    # )

                outfile_list.append(
                    {
                        "filetype": product_slug,
                        "file": tiffile,
                        "datetime": dt_valid.isoformat(),
                        "version": None,
                    }
                )
    except Exception:
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

    return outfile_list
