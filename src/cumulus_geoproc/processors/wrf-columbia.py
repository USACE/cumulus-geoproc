"""
# Weather Research and Forecasting (WRF)

A next-generation mesoscale numerical weather prediction system designed for both atmospheric research and operational forecasting applications

**details** [here](https://www.mmm.ucar.edu/weather-research-and-forecasting-model)

## WRF Columbia River Basin

**WRF Domain 3**
"""


from datetime import timezone
from pathlib import Path
import sys

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

    this_file_stem = Path(__file__).stem

    product_acquirable = {
        "DEWPNT_T": f"{this_file_stem}-dewpnt-t",
        "GROUND_T": f"{this_file_stem}-ground-t",
        "LWDOWN__": f"{this_file_stem}-lwdown",
        "PRECIPAH": f"{this_file_stem}-precipah",
        "PSTARCRS": f"{this_file_stem}-pstarcrs",
        "RH______": f"{this_file_stem}-rh",
        "SWDOWN__": f"{this_file_stem}-swdown",
        "T2______": f"{this_file_stem}-t2",
        "U10_____": f"{this_file_stem}-u10",
        "V10_____": f"{this_file_stem}-v10",
        "VAPOR_PS": f"{this_file_stem}-vapor-ps",
    }

    src_path = Path(src)
    src_name = src_path.name
    src_stem = src_path.stem

    dst_dir = Path(dst)

    try:
        if not src_stem in product_acquirable:
            raise Exception(f"'{src_stem}' not in product acquirable dictionary")

        # extract the single grid from the source and create a temporary netCDF file
        with Dataset(src, "r") as ncsrc:
            _, nrows, ncols = ncsrc.variables["var"].shape
            nctime = ncsrc.variables["time"]
            nclat = ncsrc.variables["lat"][:]
            nclon = ncsrc.variables["lon"][:]
            ullr = [nclon.min(), nclat.max(), nclon.max(), nclat.min()]
            for dt in num2date(
                nctime[:], nctime.units, only_use_cftime_datetimes=False
            ):
                dt_valid = dt.replace(tzinfo=timezone.utc)
                idx = date2index(dt, nctime)

                # TODO: Remove after testing
                if idx > 5:
                    break

                ncdst_path = dst_dir.joinpath(src_name)
                with Dataset(str(ncdst_path), "w") as ncdst:
                    # Create dimensions
                    for name, dimension in ncsrc.dimensions.items():
                        dim_size = 1 if name == "time" else dimension.size
                        ncdst.createDimension(name, dim_size)
                    # Create variables, copy data, and set attributes
                    for name, variable in ncsrc.variables.items():
                        ncdst.createVariable(name, variable.dtype, variable.dimensions)
                        if name == "var" or name == "time" or name == "times":
                            ncdst.variables[name][:] = ncsrc.variables[name][idx]
                        else:
                            ncdst.variables[name][:] = ncsrc.variables[name][:]

                        ncdst.variables[name].setncatts(ncsrc.variables[name].__dict__)

                gdal.Warp(
                    tiffile := dst_dir.joinpath(
                        ".".join(
                            [
                                product_acquirable[src_stem],
                                dt_valid.strftime("%Y%m%d%H"),
                                "tif",
                            ]
                        )
                    ).as_posix(),
                    f"NETCDF:{ncdst_path}:var",
                    format="COG",
                    srcSRS="EPSG:4326",
                    dstSRS="EPSG:4326",
                    resampleAlg="bilinear",
                    geoloc=True,
                )

                outfile_list.append(
                    {
                        "filetype": product_acquirable[src_stem],
                        "file": tiffile,
                        "datetime": dt_valid.isoformat(),
                        "version": None,
                    }
                )
    except Exception as ex:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback_details = {
            "filename": Path(exc_traceback.tb_frame.f_code.co_filename).name,
            "line number": exc_traceback.tb_lineno,
            "method": exc_traceback.tb_frame.f_code.co_name,
            "type": exc_type.__name__,
            "message": exc_value,
        }
        for k, v in traceback_details.items():
            logger.error(f"{k}: {v}")

    return outfile_list


if __name__ == "__main__":
    src = "/Users/rdcrljsg/projects/cumulus-geoproc/cumulus-geoproc-test-data/wrf-columbia/PRECIPAH.nc"
    dst = "/Users/rdcrljsg/Downloads/wrf-columbia"
    results = process(
        src=src,
        dst=dst,
    )
    for result in results:
        print(result)
