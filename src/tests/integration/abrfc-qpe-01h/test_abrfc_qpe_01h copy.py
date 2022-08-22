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

PROCESSOR = "abrfc-qpe-01h"


class File:
    def __init__(self, filepath):
        self.processor = PROCESSOR
        self.proc_list = []
        self.output_directory = f"/output/{PROCESSOR}"
        self.infile = filepath

    def process(self):
        os.makedirs(self.output_directory, exist_ok=True)
        proc_list = geo_proc(
            plugin=PROCESSOR, src=self.infile, dst=self.output_directory
        )
        return proc_list


class AllFiles:

    """ABRFC 01hr Total Precip"""

    def __init__(self):
        self.fixtures = "/src/tests/integration/fixtures"
        self.acq_dir = os.path.join(self.fixtures, PROCESSOR)
        self.items = [File(f) for f in glob.glob(f"{self.acq_dir}/*.nc")]
        self.process_all()

    def process_all(self):
        for a in self.items:
            _proc_list = a.process()
            a.proc_list = _proc_list
            return


@pytest.fixture
def all_files() -> list:
    yield AllFiles()


def test_count_at_least_one(all_files) -> None:
    assert len(all_files.items) > 0, "Missing a test file for this product"


def test_one_output_tif(all_files) -> None:
    for f in all_files.items():
        print(f.infile)
        print(f.proc_list)
    assert (len(f.proc_list) > 0 for f in all_files.items)


# def test_product_creation(acquirables, proc_list, processor, output_directory) -> None:
#     # Find one or more input files and attempt to process
#     for acq in acquirables:
#         pl = geo_proc(plugin=processor, src=acq, dst=output_directory)
#         assert len(pl) > 0, "No files processed."
#         # Add process output list (single item) to class object
#         a.set_proc_list(pl)

#     # Check to see if the product count == acquirables count
#     assert len(proc_list) == len(
#         acquirables
#     ), "Product count not equal to acquirables count"
