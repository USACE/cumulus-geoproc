"""
# Cumulus specific gdal utilities

GTiff Creation Options to be a COG:
```
"-co",
"COMPRESS=LZW",
"-co",
"COPY_SRC_OVERVIEWS=YES",
"-co",
"TILE=YES",
```
"""

import json
import os
import pathlib
import re
import subprocess
from typing import List
from pathlib import Path
from datetime import datetime, timezone

from cumulus_geoproc import logger, utils
from cumulus_geoproc.utils import cgdal
from osgeo import gdal
from osgeo_utils import gdal_calc
from osgeo_utils.samples import validate_cloud_optimized_geotiff

gdal.UseExceptions()

this = os.path.basename(__file__)


def gdal_translate_options(**kwargs):
    """
    # Return gdal translate options

    Add dictionary attributes to use those options for translate

    Adding an existing attribute in 'base' will overwright that option

    Returns
    -------
    dict
        dictionary of gdal translate options with base option(s)

    base = {
        "format": "COG",
    }
    """
    # COG driver generates overviews while GTiff uses seperate step to build them
    base = {
        "format": "COG",
    }
    return {**base, **kwargs}


def gdal_translate_w_options(
    dst: str,
    src: gdal.Dataset,
    **kwargs,
):
    """
    # GDAL Translate wrapper with base configurations

    Parameters
    ----------
    dst : str
        Output dataset
    src : gdal.Dataset
        Dataset object or a filename
    **kwargs
        User defined keyword arguments

        Default base kwargs:

            "format": "COG",
            "bandList": [1],
            "creationOptions":[
                "RESAMPLING=BILINEAR",
                "OVERVIEWS=IGNORE_EXISTING",
                "OVERVIEW_RESAMPLING=BILINEAR",
                ]
    """
    base = {
        "format": "COG",
        "bandList": [1],
        "creationOptions": [
            "RESAMPLING=BILINEAR",
            "OVERVIEWS=IGNORE_EXISTING",
            "OVERVIEW_RESAMPLING=BILINEAR",
        ],
    }
    """dict: base (default) options but can be re-asigned"""
    _kwargs = {**base, **kwargs}
    gdal.Translate(
        dst,
        src,
        **_kwargs,
    )


def gdal_translate_w_overviews(
    dst: str,
    src: gdal.Dataset,
    translate_options: dict,
    resampling: str = None,
    overviewlist: List[int] = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048],
):
    """Build overviews for the gdal dataset with the resampling algorithm provided

    If no sampling algorithm is given, only gdal.Translate() executed

    allowable resampling algorithms:
        nearest,average,rms,bilinear,gauss,cubic,cubicspline,lanczos,average_magphase,mode

    Parameters
    ----------
    dst : str
        Output dataset name
    src : gdal.Dataset
        Dataset object or a filename
    translate_options : dict
        Dictionary of creation options
    resampling : str, optional
        resampling algorithm, by default None
    overviewlist : List[int], optional
        list of integers, by default [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048]
    """

    resampling_algo = (
        "nearest",
        "average",
        "rms",
        "bilinear",
        "gauss",
        "cubic",
        "cubicspline",
        "lanczos",
        "average_magphase",
        "mode",
    )
    if resampling is not None and resampling not in resampling_algo:
        logger.debug(f"Resampling algorithm {resampling} not available")
        return False
    try:
        if resampling:
            gdal.Translate(
                f"/vsimem/{dst}",
                src,
                format="GTiff",
                creationOptions=[
                    "COMPRESS=LZW",
                    "TILED=YES",
                ],
            )
            _ds = gdal.Open(f"/vsimem/{dst}", gdal.GA_Update)
            _ds.BuildOverviews(resampling=resampling, overviewlist=overviewlist)
            gdal.Translate(
                dst,
                _ds,
                **translate_options,
            )
        else:
            gdal.Translate(
                dst,
                src,
                **translate_options,
            )
        return True
    except RuntimeError as ex:
        logger.error(f"{type(ex).__name__}: {this}: {ex}")
    finally:
        _ds = None
    return False


# get a band based on provided attributes in the metadata
def find_band(data_set: "gdal.Dataset", attr: dict = {}, regex_enabled: bool = False):
    """Return the band number

    Parameters
    ----------
    data_set : gdal.Dataset
        gdal dataset
    attr : dict, optional
        attributes matching those in the metadata, by default {}

    Returns
    -------
    int
        band number
    """
    count = data_set.RasterCount
    for b in range(1, count + 1):
        has_attr = 0
        try:
            raster = data_set.GetRasterBand(b)
            meta = raster.GetMetadata_Dict()
            for key, val in attr.items():
                if key in meta:
                    # Many grib values include regex special characters. e.g. [C] (degrees celsius)
                    # Function escapes special characters by default to avoid breaking changes by introducing re.search().
                    # Escaping special characters by default will cause this helper function to behave the same way
                    # it did previously when looking for a substring using "in".
                    _val = val
                    if not regex_enabled:
                        _val = re.escape(_val)
                    if re.search(_val, raster.GetMetadataItem(key)) is not None:
                        has_attr += 1
            if has_attr == len(attr):
                logger.debug(f"{has_attr=}")
                return b

        except RuntimeError as ex:
            logger.error(f"{type(ex).__name__}: {this}: {ex}")
            continue
        finally:
            raster = None

    return None


def band_from_json(info: json, attr: dict, rex: bool = False):
    """band_from_json _summary_

    Parameters
    ----------
    info : json
        _description_
    attr : dict
        _description_

    Returns
    -------
    _type_
        _description_
    """

    bands = info["bands"]
    for band in bands:
        has_match = 0
        meta = band["metadata"][""]
        meta_keys = set(meta.keys())
        attr_keys = set(attr.keys())
        key_intersect = meta_keys.intersection(attr_keys)

        if len(attr) == len(key_intersect):
            for key in key_intersect:
                search_pattern = attr[key] if rex else re.escape(attr[key])
                search_match = re.match(search_pattern, meta[key])
                if search_match:
                    has_match += 1
            if len(attr) == has_match:
                return band["band"]


def gdal_calculate(*args):
    """Implement gdal-utils gdal_calc CLI utility

    gdal_translate documentation:

    https://gdal.org/programs/gdal_translate.html
    """
    argv = [gdal_calc.__file__]
    argv.extend(list(args))

    logger.debug(f"Argvs: {argv=}")

    gdal_calc.main(argv)


def gdal_fillnodataval(src: str, dst: str, /, *args):
    """Implement gdal-utils gdal_fillnodata CLI utility as a subprocess

    gdal_fillnodata documentation:

    https://gdal.org/programs/gdal_fillnodata.html
    """
    argv = ["gdal_fillnodata.py"]
    argv.extend(list(args))
    argv.append(src)
    argv.append(dst)

    logger.debug(f"Argvs: {argv=}")

    try:
        result = subprocess.check_call(argv, cwd=pathlib.PurePath(src).parent)
        return result
    except subprocess.CalledProcessError as ex:
        logger.error(f"{type(ex).__name__}: {this}: {ex}")
        return result


def validate_cog(*args):
    argv = [validate_cloud_optimized_geotiff.__file__]
    argv.extend(list(args))

    logger.debug(f"Argvs: {argv=}")

    return validate_cloud_optimized_geotiff.main(argv)


def openfileGDAL(src, dst):
    # Source and Destination as Paths
    # take the source path as the destination unless defined.
    src_path = Path(src)
    if dst is None:
        dst_path = src_path.parent
    else:
        dst_path = Path(dst)

    # NOTE: Because we are already working against a copy of the acquirable file 'src',
    #       not the original archive file on AWS S3, use gdal.Open() with gdal.GA_Update
    #       (not gdal.GA_ReadOnly).
    #
    #       This allows setting Transform and Projection on the dataset so they are included
    #       in the bands that get translated out. Because 'src' is already a copy, no risk of
    #       corrupting the original file at this time. If 'src' is ever passed as a virtual
    #       path to the original file in archive (e.g. /vsis3/...), will want to revisit.
    exts = (
        ".gz",
        ".tar",
        ".zip",
        ".tar.gz",
    )

    try:
        if any([x in src for x in exts]):
            try:
                ds = gdal.Open("/vsigzip/" + src, gdal.GA_Update)
            except RuntimeError as err:
                logger.warning(err)
                logger.warning(f'gunzip "{src}" and use as source file')
                src_unzip = utils.decompress(src, str(dst_path))
                ds = gdal.Open(src_unzip, gdal.GA_Update)
        else:
            ds = gdal.Open(src, gdal.GA_Update)
    except RuntimeError as err:
        logger.warning(err)
        logger.warning(f"could not open file {src}")

    return ds, src_path, dst_path


def findsubset(ds, subsets):
    subdatasets = ds.GetSubDatasets()

    for subdataset in subdatasets:
        subsetpath, datatype = subdataset
        if all([x in datatype for x in subsets]):
            ds = gdal.Open(subsetpath)
            break
        else:
            ds = None

    if ds is None:
        raise Exception(f"Did not find the sub-dataset we are lookingfor, {subsets}")

    return ds


def getVersionDate(ds, src_path, metaVar, fileDateFormat, filedateSearch):
    # get the version
    date_created = ds.GetMetadataItem(metaVar)
    date_created_match = re.search("\\d+", date_created)
    if date_created_match:
        version_datetime = datetime.fromtimestamp(int(date_created_match[0])).replace(
            tzinfo=timezone.utc
        )
    else:
        filename = src_path.name
        date_str = re.search(filedateSearch, filename)[0]
        version_datetime = datetime.strptime(date_str, fileDateFormat).replace(
            tzinfo=timezone.utc
        )
    return version_datetime


def subsetOutFile(ds, SUBSET_NAME, dst_path, acquirable, version_datetime):
    # Get the subset metadata and the valid times as a list
    outfile_list = []
    sub_meta = ds.GetMetadata_Dict()
    valid_times_list = list(eval(sub_meta[f"{SUBSET_NAME}#validTimes"]))
    valid_times_list.sort()

    for i, t in enumerate(valid_times_list):
        # skip the zero valid time
        if i == 0:
            continue

        valid_datetime = datetime.fromtimestamp(t).replace(tzinfo=timezone.utc)

        raster_band = ds.GetRasterBand(i)

        nodata = raster_band.GetNoDataValue()

        cgdal.gdal_translate_w_options(
            tif := str(
                dst_path / f'{acquirable}.{valid_datetime.strftime("%Y%m%d_%H%M")}.tif'
            ),
            ds,
            bandList=[i],
            noData=nodata,
        )

        # validate COG
        if (validate := cgdal.validate_cog("-q", tif)) == 0:
            logger.debug(f"Validate COG = {validate}\t{tif} is a COG")

        outfile_list.append(
            {
                "filetype": acquirable,
                "file": tif,
                "datetime": valid_datetime.isoformat(),
                "version": version_datetime.isoformat(),
            },
        )
    return outfile_list


# TODO: GridProcess class
class GridProcess:
    pass
