import os
import unittest
from osgeo import gdal
from urllib.request import urlretrieve

from cumulus_geoproc.processors import geo_proc
from cumulus_geoproc.utils.cgdal import find_band


class TestHrrrTotalPrecip20220818f01(unittest.TestCase):
    """HRRR Total Precip; File from 2022-08-18; Forecast Hour 01"""

    def setUp(self) -> None:
        self.acquirable = os.path.join(
            os.path.dirname(__file__),
            "..",
            "fixtures",
            "hrrr-total-precip",
            "hrrr-total-precip-20220818",
            "hrrr.t00z.wrfsfcf01.grib2",
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
                "https://noaa-hrrr-bdp-pds.s3.amazonaws.com/hrrr.20220818/conus/hrrr.t00z.wrfsfcf01.grib2",
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
        self.assertEqual(band, 84)

    def test_at_least_one_productfile(self) -> None:
        proc_list = geo_proc(
            plugin="hrrr-total-precip", src=self.acquirable, dst=self.output_directory
        )
        self.assertGreater(len(proc_list), 0, "Empty 'products processed' list")

    def test_translated_correct_band(self) -> None:
        # Metadata of the translated band matches `attrs` passed to find_band in acquirable
        dst = os.path.join(self.output_directory)
        os.makedirs(dst, exist_ok=True)
        proc_list = geo_proc(plugin="hrrr-total-precip", src=self.acquirable, dst=dst)
        # Search the output geotif using same attrs that should be used to select it from the acquirable
        # Known geotiff should have only one band that matches attrs, so proc_list[0] is ok
        ds = gdal.Open(proc_list[0]["file"])
        attr = {
            "GRIB_ELEMENT": "APCP01",
            "GRIB_COMMENT": "precipitation",
            "GRIB_UNIT": "[kg/(m^2)]",
        }
        band = find_band(ds, attr)
        ds = None

        # If find_band(...) in this case returns None, the wrong band was translated out of the acquirable by the processor plugin
        self.assertIsNotNone(band)


if __name__ == "__main__":
    unittest.main()
