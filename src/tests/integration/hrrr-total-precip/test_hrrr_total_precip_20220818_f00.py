import os
from osgeo import gdal
from urllib.request import urlretrieve

from cumulus_geoproc.processors import geo_proc
from cumulus_geoproc.utils import cgdal
from cumulus_geoproc.utils.cgdal import find_band


class TestHrrrTotalPrecip20220818f00:
    """HRRR Total Precip; File from 2022-08-18; Forecast Hour 00"""

    def setup_method(self) -> None:
        self.acquirable = os.path.join(
            os.path.dirname(__file__),
            "..",
            "fixtures",
            "hrrr-total-precip",
            "hrrr-total-precip-20220818",
            "hrrr.t00z.wrfsfcf00.grib2",
        )
        # Create parent directory to download acquirable if it dos not exist
        os.makedirs(os.path.dirname(self.acquirable), exist_ok=True)
        # Output Directory
        self.output_directory = "/output/hrrr-total-precip/hrrr-total-precip-20220818"
        os.makedirs(self.output_directory, exist_ok=True)
        # If acquirable not stored in `cumulus-geoproc-test-data`; download it
        if not os.path.isfile(self.acquirable):
            # @todo; change link below to persistent archive link to acquire file
            urlretrieve(
                "https://noaa-hrrr-bdp-pds.s3.amazonaws.com/hrrr.20220818/conus/hrrr.t00z.wrfsfcf00.grib2",
                self.acquirable,
            )

    def teardown_method(self) -> None:
        pass

    def test_input_file_exists(self) -> None:
        # self.assertTrue(os.path.isfile(self.acquirable))
        assert os.path.isfile(self.acquirable), "Input file not found"

    def test_find_correct_band(self) -> None:
        # Get Band using attributes from processor
        attr = {
            "GRIB_ELEMENT": "APCP01",
            "GRIB_COMMENT": "precipitation",
            "GRIB_UNIT": "[kg/(m^2)]",
        }
        ds = gdal.Open(self.acquirable)
        # No band should be returned for 00 hour file
        assert find_band(ds, attr) is None, "Band is not None"

    def test_at_least_one_productfile(self) -> None:
        proc_list = geo_proc(
            plugin="hrrr-total-precip", src=self.acquirable, dst=self.output_directory
        )
        # self.assertGreater(len(proc_list), 0, "Product not processed.")
        assert len(proc_list) == 0, "Unexpected product was processed."
