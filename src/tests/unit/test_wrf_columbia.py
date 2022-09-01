"""
# Pytests for WRF Columbia
"""
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest
from cumulus_geoproc.processors import geo_proc

# TODO: Add additional tests
# @pytest.mark.skip(reason="Local testing only due to test file size")
def test_precipah():
    fixtures = Path("/src/tests/integration/fixtures")

    tmpdir = TemporaryDirectory()

    processed = geo_proc(
        plugin="wrf-columbia",
        src=str(fixtures / "wrf-columbia-1980w-precipah.nc"),
        dst=tmpdir.name,
    )

    assert len(processed) > 0, "Processor did not produce at least one product file"
