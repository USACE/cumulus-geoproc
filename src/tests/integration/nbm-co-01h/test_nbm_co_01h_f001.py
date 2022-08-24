import os
import sys
from osgeo import gdal
from datetime import datetime, timedelta
from urllib.request import urlretrieve
import pytest

from cumulus_geoproc.processors import geo_proc
from cumulus_geoproc.utils import cgdal
from cumulus_geoproc.utils.cgdal import find_band


import importlib
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
testutils = importlib.import_module("default-test-suite.utils")
default_tests = importlib.import_module("default-test-suite.test_default_test_suite")


@pytest.fixture(scope="module")
def processed():
        _info = testutils.nbm_co_01h_fixture_info_factory("00", "001")
        return testutils.ProcessorResult(*_info)


AIRTEMP_BAND_SEARCH_ATTR = {
    "GRIB_COMMENT": "Temperature \\[C\\]",
    "GRIB_ELEMENT": "^T$",
    "GRIB_SHORT_NAME": "2\\-HTGL",
    "GRIB_UNIT": "\\[C\\]",
}

PRECIP_BAND_SEARCH_ATTR = {
    "GRIB_ELEMENT": "QPF01",
    "GRIB_SHORT_NAME": "0\\-SFC",
}


def test_find_airtemp_band(processed) -> None:
    # Get Band using attributes from processor

    # GRIB_COMMENT=Temperature [C]
    ds = gdal.Open(processed.infile)
    band = find_band(ds, AIRTEMP_BAND_SEARCH_ATTR, True)
    ds = None
    assert band == 54, "find_band selected incorrect band"


def test_find_precip_band(processed) -> None:
    # Get Band using attributes from processor

    ds = gdal.Open(processed.infile)
    band = find_band(ds, PRECIP_BAND_SEARCH_ATTR, True)
    ds = None
    assert band == 46, "find_band selected incorrect band"


def test_output_two_productfiles(processed) -> None:
    proc_list = geo_proc(
        plugin="nbm-co-01h", src=processed.infile, dst=processed.output_directory
    )
    assert len(proc_list) == 2, f"unexpected number of productfiles: {len(proc_list)}"
   
        

    # def test_translated_correct_airtemp_band(self) -> None:
    #     # Metadata of the translated band matches `attrs` passed to find_band in acquirable
    #     dst = os.path.join(self.output_directory)
    #     os.makedirs(dst, exist_ok=True)
    #     proc_list = geo_proc(plugin="nbm-co-01h", src=self.acquirable, dst=dst)
    #     # Search the output geotif using same attrs that should be used to select it from the acquirable
    #     # Known geotiff should have at most two bands, so proc_list[0] is airtemp, proclist[1] is precip
    #     ds = gdal.Open(proc_list[0]["file"])
    #     # Regex in find_band search strings toggled on via True
    #     band = find_band(ds, self.AIRTEMP_BAND_SEARCH_ATTR, True)
    #     ds = None
    #     # If find_band(...) in this case returns None, the wrong band was translated out of the acquirable by the processor plugin
    #     assert band is not None, f"Expected airtemp band not found in output tif: {proc_list[0]['file']}"


    # def test_translated_correct_precip_band(self) -> None:
    #     # Metadata of the translated band matches `attrs` passed to find_band in acquirable
    #     dst = os.path.join(self.output_directory)
    #     os.makedirs(dst, exist_ok=True)
    #     proc_list = geo_proc(plugin="nbm-co-01h", src=self.acquirable, dst=dst)
    #     # Search the output geotif using same attrs that should be used to select it from the acquirable
    #     # Known geotiff should have at most two bands, so proc_list[0] is airtemp, proclist[1] is precip
    #     ds = gdal.Open(proc_list[1]["file"])
    #     # Regex in find_band search strings toggled on via True
    #     band = find_band(ds, self.PRECIP_BAND_SEARCH_ATTR, True)
    #     ds = None
    #     # If find_band(...) in this case returns None, the wrong band was translated out of the acquirable by the processor plugin
    #     assert band is not None, f"Expected precip band not found in output tif: {proc_list[1]['file']}"
