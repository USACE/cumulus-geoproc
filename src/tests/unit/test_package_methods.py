""" 
Unit test methods for cumulus-geoproc package
"""

import json
from pathlib import Path
import re


from cumulus_geoproc.utils import cgdal

# gdal info from file
GDAL_INFO = Path(__file__).parent.joinpath("gdal_info_hrrr.json").resolve()


def test_gdal_find_band():
    """test_gdal_find_band"""
    attr = {
        "GRIB_COMMENT": "01 hr Total precipitation \\[kg/\\(m\\^2\\)\\]",
        "GRIB_ELEMENT": "APCP01",
        "GRIB_UNIT": re.escape("[kg/(m^2)]"),
    }

    with GDAL_INFO.open("r", encoding="utf-8") as fptr:
        gdal_info = json.load(fptr)

    band_number = cgdal.band_from_json(gdal_info, attr)

    assert band_number == 90, f"Band number {band_number} != 90"
