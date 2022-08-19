import os
import unittest
from urllib.request import urlretrieve

from cumulus_geoproc.processors import geo_proc
from cumulus_geoproc.utils.cgdal import find_band
from osgeo import gdal


class TestHrrrTotalPrecip20220818f00(unittest.TestCase):
    """HRRR Total Precip; File from 2022-08-18; Forecast Hour 00"""

    def setUp(self) -> None:
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

    def tearDown(self) -> None:
        pass

    def test_input_file_exists(self) -> None:
        self.assertTrue(os.path.isfile(self.acquirable))

    def test_find_correct_band(self) -> None:
        # Get Band using attributes from processor
        attr = {
            "GRIB_ELEMENT": "APCP01",
            "GRIB_COMMENT": "precipitation",
            "GRIB_UNIT": "[kg/(m^2)]",
        }
        ds = gdal.Open(self.acquirable)
        band = find_band(ds, attr)
        ds = None
        # Get the band
        self.assertIsNone(band)

    def test_at_least_one_productfile(self) -> None:
        proc_list = geo_proc(
            plugin="hrrr-total-precip", src=self.acquirable, dst=self.output_directory
        )
        self.assertListEqual(proc_list, [], "Product list NOT empty; band found")


if __name__ == "__main__":
    unittest.main()
