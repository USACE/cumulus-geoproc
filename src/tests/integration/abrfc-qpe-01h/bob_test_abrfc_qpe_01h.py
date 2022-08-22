import os, glob, re
from datetime import datetime
import pytest

from osgeo import gdal
import numpy as np

# from urllib.request import urlretrieve
from netCDF4 import Dataset

from cumulus_geoproc.processors import geo_proc
from cumulus_geoproc.utils import cgdal

# Prevent gdal from creating *.aux.xml stat files
os.environ["GDAL_PAM_ENABLED"] = "NO"

"""
print(ncds.variables)

{'Total_precipitation': <class 'netCDF4._netCDF4.Variable'>
float32 Total_precipitation(time, y, x)
    units: kg/m^2
    standard_name: precipitation_amount
    long_name: 01 hr Precip
    cell_methods: time: sum
    missing_value: -9999.0
    grid_mapping: Polar_Stereographic
    coordinates: time y x 
    udunits: millimeter
    uiname: 01 hr precip estimate
    valid_range: [   0. 1000.]
    _FillValue: -9999.0
    _n3D: 0
    levels: SFC
"""


class AbrfcQpe01h:

    """ABRFC 01hr Total Precip"""

    def __init__(self):
        self._processor = "abrfc-qpe-01h"
        self._fixtures = "/src/tests/integration/fixtures"
        self._acq_dir = os.path.join(self._fixtures, self._processor)
        self._acquirables = glob.glob(f"{self._acq_dir}/*.nc")
        self._proc_list = []
        self._output_directory = f"/output/{self._processor}"

    def acquirables(self) -> list:
        return self._acquirables

    def processor(self) -> str:
        return self._processor

    def output_directory(self) -> str:
        os.makedirs(self._output_directory, exist_ok=True)
        return self._output_directory

    def proc_list(self) -> list:
        return self._proc_list

    def set_proc_list(self, item_list):
        self._proc_list.extend(item_list)


# Instantiate the class object
a = AbrfcQpe01h()


@pytest.fixture
def acquirables() -> list:
    yield a.acquirables()


@pytest.fixture
def processor() -> str:
    yield a.processor()


@pytest.fixture
def proc_list() -> list:
    yield a.proc_list()


@pytest.fixture
def output_directory() -> str:
    yield a.output_directory()


def test_acquirable_count_at_least_one(acquirables) -> None:
    assert len(acquirables) > 0, "No acquirable files found"


def test_product_creation(acquirables, proc_list, processor, output_directory) -> None:
    # Find one or more input files and attempt to process
    for acq in acquirables:
        pl = geo_proc(plugin=processor, src=acq, dst=output_directory)
        assert len(pl) > 0, "No files processed."
        # Add process output list (single item) to class object
        a.set_proc_list(pl)

    # Check to see if the product count == acquirables count
    assert len(proc_list) == len(
        acquirables
    ), "Product count not equal to acquirables count"


def test_product_is_valid_cog(proc_list) -> None:
    # Verify output files are valid COG
    for product in proc_list:
        assert cgdal.validate_cog("-q", product["file"]) == 0, "Invalid COG"


def test_compare_acquirable_product_stats(acquirables, proc_list) -> None:
    for idx, acq in enumerate(acquirables):
        with Dataset(acq, "r") as ncds:

            np_data = np.array(
                np.squeeze(ncds.variables["Total_precipitation"][:].data),
                dtype="float64",
            )
            src_min = np.min(np_data)
            src_max = round(np.max(np_data), 2)
            assert src_min == 0, "Minimum data value not zero."
            # Assume values should be less than 6 inches in a single hour
            # Units are in millimeters
            assert (
                src_max <= 153
            ), f"Maximum data value greater than 153 mm (6 in).  Actual value: {src_max}"

        # Get product stats and compare to acquirable
        ds = gdal.Open(proc_list[idx]["file"], gdal.GA_ReadOnly)
        band = ds.GetRasterBand(1)
        band.ComputeStatistics(0)
        dst_min = band.GetMinimum()
        dst_max = round(band.GetMaximum(), 2)
        ds = None

        # print(f"Src Min: {src_min}")
        # print(f"Dst Min: {dst_min}")
        assert src_min == dst_min, "Stats: Min values do not match"

        # print(f"Src Max: {src_max}")
        # print(f"Dst Max: {dst_max}")
        assert src_max == dst_max, "Stats: Max values do not match"


def test_product_version(proc_list) -> None:
    # Version should be None
    for product in proc_list:
        assert product["version"] is None, "Version is not None"


def test_product_file_contains_datetime(proc_list) -> None:
    # Find the Year Month Day Hour in the filename
    for product in proc_list:
        match = re.search(r"\d{4}\d{2}\d{2}\d{2}", os.path.basename(product["file"]))
        # Verify the datetime string is legit
        assert datetime.strptime(
            match.group(), "%Y%M%d%H"
        ), "Output file datetime is not valid"
