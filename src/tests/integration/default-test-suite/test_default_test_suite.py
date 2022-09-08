import os, glob, re
from datetime import datetime
import hashlib
import pytest

# from osgeo import gdal
# import numpy as np

# # from urllib.request import urlretrieve
# from netCDF4 import Dataset

from cumulus_geoproc.utils import cgdal

from config import FIXTURE_INFO, DATE_FORMATS
from utils import ProcessorResult


# Prevent gdal from creating *.aux.xml stat files
os.environ["GDAL_PAM_ENABLED"] = "NO"


# scope="module" results in processing being computed once, reused in subsequent tests
# see https://docs.pytest.org/en/6.2.x/fixture.html#scope-sharing-fixtures-across-classes-modules-packages-or-session
@pytest.fixture(scope="module")
def processed():
    return [ProcessorResult(*entry) for entry in FIXTURE_INFO]


###############################################################################################################
# TEST CASES
###############################################################################################################


def test_infile_exists(processed) -> None:
    for p in processed:
        assert os.path.isfile(p.infile), "Specified test file does not exist"


def test_productfile_at_least_one(processed) -> None:
    for p in processed:
        assert len(p.result) > 0, "Processor did not produce at least one productfile"


def test_productfile_file_exists_on_disk(processed) -> None:
    for p in processed:
        for r in p.result:
            file = r["file"]
            assert os.path.isfile(file), f"Productfile does not exist on disk: {file}"


def test_productfile_version_is_none(processed) -> None:
    # Version should be None, or a version that is not the default version
    for p in processed:
        for r in p.result:
            assert r["version"] is None or not r["version"].startswith(
                "1111-11-11T11:11:11"
            ), """
            Version explicitly set to default version in database.
            Recommend setting version = None and letting the database handle this
            """


def test_productfile_filename_is_unique(processed) -> None:
    # Catch the case where multiple output files have the same filename.
    # When this happens, the second output file overwrites the first one
    # causing unexpected results
    for p in processed:
        filenames = [r["file"] for r in p.result]
        for filename in filenames:
            assert (
                sum([1 for _f in filenames if _f == filename]) == 1
            ), f"non-unique filename in output: {p.processor}; {filename}"


def test_productfile_hash_is_unique(processed):
    # When multiple output files are generated, verify the contents
    # of each file is unique
    for p in processed:
        hashes = [
            hashlib.md5(open(r["file"], "rb").read()).hexdigest() for r in p.result
        ]
        for h in hashes:
            assert (
                sum([1 for _h in hashes if _h == h]) == 1
            ), f"non-unique file hash in output: {p.processor}; {h}"


def test_productfile_filename_has_datetime(processed) -> None:
    for p in processed:
        for r in p.result:
            match = None
            for fmt, regex in DATE_FORMATS:
                match = re.search(regex, os.path.basename(r["file"]))
                if match:
                    # Note - trying to use: assert datetime.strptime(match.group(), fmt)
                    # will not work as intended.  The errors produced are not user friendly
                    # and helpful when tracing down which file and format caused the issue
                    err = None

                    # Try to create a datetime object using the matched date string
                    # and the format (which matched from the regex)

                    try:
                        dt_obj = datetime.strptime(match.group(), fmt)
                    except ValueError:
                        err = f"output filename does not contain valid datetime string: {r['file']}."
                        err += f"  Unable to convert {match.group()} into a valid datetime format using {fmt}"

                    assert err == None, "Invalid date format"
                    assert dt_obj.year >= 1900, f"Year {dt_obj.year} is not >= 1900"
                    break

            assert (
                match is not None
            ), f"output filename does not contain datetime string: {r['file']}"


def test_productfile_is_valid_cog(processed) -> None:
    for p in processed:
        for r in p.result:
            file = r["file"]
            assert cgdal.validate_cog("-q", file) == 0, f"failed validate_cog: {file}"


def test_stats_max_reasonable(processed) -> None:
    # for p in processed:
    #     if p.reasonable_max is not None:
    #         assert p.reasonable_max < p.max, "maximum value in grid is unreasonably high"
    pass


def test_stats_min_reasonable(processed) -> None:
    # for p in processed:
    #     if p.reasonable_min is not None:
    #         assert p.reasonable_min < p.min, "minimum value in grid is unreasonably low"
    pass
