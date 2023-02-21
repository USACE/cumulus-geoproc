"""
Methods testing many aspects of a gridded product
"""

import hashlib
from datetime import datetime
from pathlib import Path

from osgeo import gdal

from cumulus_geoproc.processors import geo_proc
from cumulus_geoproc.utils import cgdal

from .conftest import LOCAL_TEST_PRODUCTS, OUTPUT_PRODUCTS


def test_file_exists(products):
    """Test file exists"""
    for prod in products:
        _path = LOCAL_TEST_PRODUCTS.joinpath(prod["local_source"])
        assert _path.exists(), f"File does not exist: {_path}"


def test_product_has_output(products, tiff_files):
    """Test product produces at least one output"""
    for prod in products:
        _path = LOCAL_TEST_PRODUCTS.joinpath(prod["local_source"]).as_posix()
        outputs = geo_proc(
            plugin=prod["plugin"],
            src=_path,
            dst=str(tiff_files),
        )
        OUTPUT_PRODUCTS.append(outputs)
        assert len(outputs) > 0, f"No output for {_path}"


def test_correct_band(products):
    for prod in products:
        _path = LOCAL_TEST_PRODUCTS.joinpath(prod["local_source"]).as_posix()
        if "attr" in prod:
            band_attrs = prod["attr"]
            dset = gdal.Open(_path)
            for band_num, band_attr in band_attrs.items():
                band_found = cgdal.find_band(dset, band_attr)
                assert band_found == int(
                    band_num
                ), f"Band number {band_found} != {band_num} for {_path}"
            dset = None


def test_product_exists():
    """Make sure the produced product exits"""
    for prods in OUTPUT_PRODUCTS:
        for prod in prods:
            _path = prod["file"]
            assert Path(_path).exists(), f"Product doesn't exist: {prod}"


def test_product_version(products):
    """Test the version is assign correctly for the type, observed or forcaste"""
    for i, prod in enumerate(products):
        vtype = prod["vtype"]
        prods = OUTPUT_PRODUCTS[i]
        for prod in prods:
            if vtype == "observed":
                assert (
                    prod["version"] is None
                ), f"Version has a date and should be None: {prod}"
            elif vtype == "forecast":
                assert (
                    prod["version"] is not None
                ), f"Version is None and needs a date: {prod}"
            else:
                assert (
                    vtype != "observed"
                ), f"Version type not correctly defined as {vtype}"
                assert (
                    vtype != "forecast"
                ), f"Version type not correctly defined as {vtype}"


def test_product_datetime():
    """Test the output products have correct datetime format"""
    for prods in OUTPUT_PRODUCTS:
        for prod in prods:
            dtstr = prod["datetime"]
            if dtstr:
                dtime = datetime.fromisoformat(dtstr)
                assert dtime.isoformat() == dtstr, f"Datetime is not ISO format: {prod}"


def test_product_version_datetime():
    """Test the output products have correct version datetime format"""
    for prods in OUTPUT_PRODUCTS:
        for prod in prods:
            dtstr = prod["version"]
            if dtstr is not None:
                dtime = datetime.fromisoformat(dtstr)
                assert dtime.isoformat() == dtstr, f"Datetime is not ISO format: {prod}"


def test_product_unique_output():
    """Test the product output does not have duplicate names"""
    for prods in OUTPUT_PRODUCTS:
        number_outputs = len(prods)
        number_files = len(set(prod["file"] for prod in prods))
        assert (
            number_outputs == number_files
        ), f"More outputs than number of files: {prods}"


def test_cog_valid():
    """Test the resulting product is a valid COG"""
    for prods in OUTPUT_PRODUCTS:
        for prod in prods:
            cog = prod["file"]
            assert cgdal.validate_cog("-q", cog) == 0, f"Product not a COG: {cog}"


def test_cog_unique():
    """Test the outputs are unique"""
    for prods in OUTPUT_PRODUCTS:
        hasher = hashlib.md5()
        all_dgst = []
        for prod in prods:
            fname = Path(prod["file"])
            with fname.open("rb") as fptr:
                data = fptr.read()
                hasher.update(data)
                dgst = hasher.hexdigest()
                all_dgst.append(dgst)
        assert len(all_dgst) == len(
            set(all_dgst)
        ), f"Not all products unique in {prods}"


# def test_teardown():
#     """Teardown the files created"""
#     for prods in OUTPUT_PRODUCTS:
#         for prod in prods:
#             _path = Path(prod["file"])
#             _path.unlink(True)
