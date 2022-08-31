"""
# Pytests for WRF Columbia
"""

from pathlib import Path
from tempfile import TemporaryDirectory

import pytest
from cumulus_geoproc.processors import geo_proc

# TODO: Add additional tests
@pytest.mark.skip(reason="Local testing only due to test file size")
def test_dewpnt_t():
    fixtures = Path("/src/tests/integration/fixtures")
    dewpnt_t = Path(
        "wrfout/d03fmt/reconstruction/2000s/ncf/wrf-columbia-2000s-dewpnt_t.nc"
    )

    tmpdir = TemporaryDirectory()

    processed = geo_proc(
        plugin="wrf-columbia",
        src=str(fixtures / dewpnt_t),
        dst=tmpdir.name,
    )

    assert len(processed) > 0, "Processor did not produce at least one product file"
