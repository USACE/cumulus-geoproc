import os
import unittest
from cumulus_geoproc.processors import geo_proc


class TestProcessors(unittest.TestCase):
    def setUp(self) -> None:
        self.test_dir = os.path.dirname(__file__)
        self.fixtures = os.path.join(self.test_dir, "fixtures")
        self.ftype = (
            "bil.zip",
            "grb",
            "grb2",
            "grb.gz",
            "grib",
            "grib.gz",
            "grib2",
            "grib2.gz",
            "nc",
            "nc.gz",
            "tar",
        )

    # TODO: remove files and directories with better code
    @unittest.skip("Skipping tearDown to see if files are created.")
    def tearDown(self) -> None:
        dirpath = os.walk(self.fixtures)
        for dirpath, dirnames, filenames in os.walk(self.fixtures):
            # delete all the files generated
            for file in filenames:
                path_ = os.path.join(dirpath, file)
                if not file.endswith(self.ftype):
                    try:
                        os.remove(path_)
                    except OSError as err:
                        print(err)

    def test_abrfc_qpe_01h(self) -> None:
        acquire = "abrfc-qpe-01h"
        pdir = os.path.join(self.fixtures, acquire)

        for file in os.listdir(pdir):
            if file.endswith(self.ftype):
                proc_list = geo_proc(
                    plugin=acquire,
                    src=os.path.join(pdir, file),
                )
                self.assertGreater(len(proc_list), 0, "Product not processed.")

    def test_cbrfc_mpe(self) -> None:
        acquire = "cbrfc-mpe"
        pdir = os.path.join(self.fixtures, acquire)

        for file in os.listdir(pdir):
            if file.endswith(self.ftype):
                proc_list = geo_proc(
                    plugin=acquire,
                    src=os.path.join(pdir, file),
                )
                self.assertGreater(len(proc_list), 0, "Product not processed.")

    def test_cnrfc_qpe_06h(self) -> None:
        acquire = "cnrfc-qpe-06h"
        pdir = os.path.join(self.fixtures, acquire)

        for file in os.listdir(pdir):
            if file.endswith(self.ftype):
                proc_list = geo_proc(
                    plugin=acquire,
                    src=os.path.join(pdir, file),
                )
                self.assertGreater(len(proc_list), 0, "Product not processed.")

    def test_hrrr_total_precip(self) -> None:
        acquire = "hrrr-total-precip"
        pdir = os.path.join(self.fixtures, acquire)

        for file in os.listdir(pdir):
            if file.endswith(self.ftype):
                proc_list = geo_proc(
                    plugin=acquire,
                    src=os.path.join(pdir, file),
                )
                self.assertGreater(len(proc_list), 0, "Product not processed.")

    def test_lmrfc_qpe_01h(self) -> None:
        acquire = "lmrfc-qpe-01h"
        pdir = os.path.join(self.fixtures, acquire)

        for file in os.listdir(pdir):
            if file.endswith(self.ftype):
                proc_list = geo_proc(
                    plugin=acquire,
                    src=os.path.join(pdir, file),
                )
                self.assertGreater(len(proc_list), 0, "Product not processed.")

    def test_lmrfc_qpf_06h(self) -> None:
        acquire = "lmrfc-qpf-06h"
        pdir = os.path.join(self.fixtures, acquire)

        for file in os.listdir(pdir):
            if file.endswith(self.ftype):
                proc_list = geo_proc(
                    plugin=acquire,
                    src=os.path.join(pdir, file),
                )
                self.assertGreater(len(proc_list), 0, "Product not processed.")

    def test_marfc_nbmt_01h(self) -> None:
        acquire = "marfc-nbmt-01h"
        pdir = os.path.join(self.fixtures, acquire)

        for file in os.listdir(pdir):
            if file.endswith(self.ftype):
                proc_list = geo_proc(
                    plugin=acquire,
                    src=os.path.join(pdir, file),
                )
                self.assertGreater(len(proc_list), 0, "Product not processed.")

    def test_marfc_rtmat_01h(self) -> None:
        acquire = "marfc-rtmat-01h"
        pdir = os.path.join(self.fixtures, acquire)

        for file in os.listdir(pdir):
            if file.endswith(self.ftype):
                proc_list = geo_proc(
                    plugin=acquire,
                    src=os.path.join(pdir, file),
                )
                self.assertGreater(len(proc_list), 0, "Product not processed.")

    def test_mbrfc_krf_fct_airtemp_01h(self) -> None:
        acquire = "mbrfc-krf-fct-airtemp-01h"
        pdir = os.path.join(self.fixtures, acquire)

        for file in os.listdir(pdir):
            if file.endswith(self.ftype):
                proc_list = geo_proc(
                    plugin=acquire,
                    src=os.path.join(pdir, file),
                )
                self.assertGreater(len(proc_list), 0, "Product not processed.")

    def test_mbrfc_krf_qpe_01h(self) -> None:
        acquire = "mbrfc-krf-qpe-01h"
        pdir = os.path.join(self.fixtures, acquire)

        for file in os.listdir(pdir):
            if file.endswith(self.ftype):
                proc_list = geo_proc(
                    plugin=acquire,
                    src=os.path.join(pdir, file),
                )
                self.assertGreater(len(proc_list), 0, "Product not processed.")

    def test_mbrfc_krf_qpf_06h(self) -> None:
        acquire = "mbrfc-krf-qpf-06h"
        pdir = os.path.join(self.fixtures, acquire)

        for file in os.listdir(pdir):
            if file.endswith(self.ftype):
                proc_list = geo_proc(
                    plugin=acquire,
                    src=os.path.join(pdir, file),
                )
                self.assertGreater(len(proc_list), 0, "Product not processed.")

    def test_naefs_mean_06h(self) -> None:
        acquire = "naefs-mean-06h"
        pdir = os.path.join(self.fixtures, acquire)

        for file in os.listdir(pdir):
            if file.endswith(self.ftype):
                proc_list = geo_proc(
                    plugin=acquire,
                    src=os.path.join(pdir, file),
                )
                self.assertGreater(len(proc_list), 0, "Product not processed.")

    def test_nbm_co_01h(self) -> None:
        acquire = "nbm-co-01h"
        pdir = os.path.join(self.fixtures, acquire)

        for file in os.listdir(pdir):
            if file.endswith(self.ftype):
                proc_list = geo_proc(
                    plugin=acquire,
                    src=os.path.join(pdir, file),
                )
                self.assertGreater(len(proc_list), 0, "Product not processed.")

    def test_ncep_mrms_v12_msqpe01h_p1_alaska(self) -> None:
        acquire = "ncep-mrms-v12-msqpe01h-p1-alaska"
        pdir = os.path.join(self.fixtures, acquire)

        for file in os.listdir(pdir):
            if file.endswith(self.ftype):
                proc_list = geo_proc(
                    plugin=acquire,
                    src=os.path.join(pdir, file),
                )
                self.assertGreater(len(proc_list), 0, "Product not processed.")

    def test_ncep_mrms_v12_msqpe01h_p2_alaska(self) -> None:
        acquire = "ncep-mrms-v12-msqpe01h-p2-alaska"
        pdir = os.path.join(self.fixtures, acquire)

        for file in os.listdir(pdir):
            if file.endswith(self.ftype):
                proc_list = geo_proc(
                    plugin=acquire,
                    src=os.path.join(pdir, file),
                )
                self.assertGreater(len(proc_list), 0, "Product not processed.")

    def test_ncep_mrms_v12_msqpe01h_p1_carib(self) -> None:
        acquire = "ncep-mrms-v12-msqpe01h-p1-carib"
        pdir = os.path.join(self.fixtures, acquire)

        for file in os.listdir(pdir):
            if file.endswith(self.ftype):
                proc_list = geo_proc(
                    plugin=acquire,
                    src=os.path.join(pdir, file),
                )
                self.assertGreater(len(proc_list), 0, "Product not processed.")

    def test_ncep_mrms_v12_msqpe01h_p2_carib(self) -> None:
        acquire = "ncep-mrms-v12-msqpe01h-p2-carib"
        pdir = os.path.join(self.fixtures, acquire)

        for file in os.listdir(pdir):
            if file.endswith(self.ftype):
                proc_list = geo_proc(
                    plugin=acquire,
                    src=os.path.join(pdir, file),
                )
                self.assertGreater(len(proc_list), 0, "Product not processed.")

    def test_ncep_mrms_v12_multisensor_qpe_01h_pass1(self) -> None:
        acquire = "ncep-mrms-v12-multisensor-qpe-01h-pass1"
        pdir = os.path.join(self.fixtures, acquire)

        for file in os.listdir(pdir):
            if file.endswith(self.ftype):
                proc_list = geo_proc(
                    plugin=acquire,
                    src=os.path.join(pdir, file),
                )
                self.assertGreater(len(proc_list), 0, "Product not processed.")

    def test_ncep_mrms_v12_multisensor_qpe_01h_pass2(self) -> None:
        acquire = "ncep-mrms-v12-multisensor-qpe-01h-pass2"
        pdir = os.path.join(self.fixtures, acquire)

        for file in os.listdir(pdir):
            if file.endswith(self.ftype):
                proc_list = geo_proc(
                    plugin=acquire,
                    src=os.path.join(pdir, file),
                )
                self.assertGreater(len(proc_list), 0, "Product not processed.")

    def test_ncep_rtma_ru_anl_airtemp(self) -> None:
        acquire = "ncep-rtma-ru-anl-airtemp"
        pdir = os.path.join(self.fixtures, acquire)

        for file in os.listdir(pdir):
            if file.endswith(self.ftype):
                proc_list = geo_proc(
                    plugin=acquire,
                    src=os.path.join(pdir, file),
                )
                self.assertGreater(len(proc_list), 0, "Product not processed.")

    def test_ncep_stage4_mosaic_01h(self) -> None:
        acquire = "ncep-stage4-mosaic-01h"
        pdir = os.path.join(self.fixtures, acquire)

        for file in os.listdir(pdir):
            if file.endswith(self.ftype):
                proc_list = geo_proc(
                    plugin=acquire,
                    src=os.path.join(pdir, file),
                )
                self.assertGreater(len(proc_list), 0, "Product not processed.")

    def test_ncep_stage4_mosaic_06h(self) -> None:
        acquire = "ncep-stage4-mosaic-06h"
        pdir = os.path.join(self.fixtures, acquire)

        for file in os.listdir(pdir):
            if file.endswith(self.ftype):
                proc_list = geo_proc(
                    plugin=acquire,
                    src=os.path.join(pdir, file),
                )
                self.assertGreater(len(proc_list), 0, "Product not processed.")

    def test_ncep_stage4_mosaic_24h(self) -> None:
        acquire = "ncep-stage4-mosaic-24h"
        pdir = os.path.join(self.fixtures, acquire)

        for file in os.listdir(pdir):
            if file.endswith(self.ftype):
                proc_list = geo_proc(
                    plugin=acquire,
                    src=os.path.join(pdir, file),
                )
                self.assertGreater(len(proc_list), 0, "Product not processed.")

    # def test_ncrfc_fmat_01h(self) -> None:
    #     acquire = ""

    def test_ncrfc_mpe_01h(self) -> None:
        acquire = "ncrfc-mpe-01h"
        pdir = os.path.join(self.fixtures, acquire)

        for file in os.listdir(pdir):
            if file.endswith(self.ftype):
                proc_list = geo_proc(
                    plugin=acquire,
                    src=os.path.join(pdir, file),
                )
                self.assertGreater(len(proc_list), 0, "Product not processed.")

    def test_ncrfc_rtmat_01h(self) -> None:
        acquire = "ncrfc-rtmat-01h"
        pdir = os.path.join(self.fixtures, acquire)

        for file in os.listdir(pdir):
            if file.endswith(self.ftype):
                proc_list = geo_proc(
                    plugin=acquire,
                    src=os.path.join(pdir, file),
                )
                self.assertGreater(len(proc_list), 0, "Product not processed.")

    # def test_ndfd_conus_airtemp(self) -> None:
    #     acquire = "ndfd-conus-airtemp"

    # def test_ndfd_conus_qpf_06h(self) -> None:
    #     acquire = "ndfd-conus-qpf-06h"

    # def test_ndgd_leia98_precip(self) -> None:
    #     acquire = "ndgd-leia98-precip"

    # def test_ndgd_ltia98_airtemp(self) -> None:
    #     acquire = "ndgd-ltia98-airtemp"

    # def test_nohrsc_snodas_assimilated(self) -> None:
    #     acquire = "nohrsc-snodas-assimilated"

    def test_nohrsc_snodas_unmasked(self) -> None:
        acquire = "nohrsc-snodas-unmasked"
        pdir = os.path.join(self.fixtures, acquire)

        for file in os.listdir(pdir):
            if file.endswith(self.ftype):
                proc_list = geo_proc(
                    plugin=acquire,
                    src=os.path.join(pdir, file),
                )
                self.assertGreater(len(proc_list), 0, "Product not processed.")

    def test_prism_ppt_early(self) -> None:
        acquire = "prism-ppt-early"
        pdir = os.path.join(self.fixtures, acquire)

        for file in os.listdir(pdir):
            if file.endswith(self.ftype):
                proc_list = geo_proc(
                    plugin=acquire,
                    src=os.path.join(pdir, file),
                )
                self.assertGreater(len(proc_list), 0, "Product not processed.")

    def test_prism_ppt_stable(self) -> None:
        acquire = "prism-ppt-stable"
        pdir = os.path.join(self.fixtures, acquire)

        for file in os.listdir(pdir):
            if file.endswith(self.ftype):
                proc_list = geo_proc(
                    plugin=acquire,
                    src=os.path.join(pdir, file),
                )
                self.assertGreater(len(proc_list), 0, "Product not processed.")

    def test_prism_tmax_early(self) -> None:
        acquire = "prism-tmax-early"
        pdir = os.path.join(self.fixtures, acquire)

        for file in os.listdir(pdir):
            if file.endswith(self.ftype):
                proc_list = geo_proc(
                    plugin=acquire,
                    src=os.path.join(pdir, file),
                )
                self.assertGreater(len(proc_list), 0, "Product not processed.")

    def test_prism_tmax_stable(self) -> None:
        acquire = "prism-tmax-stable"
        pdir = os.path.join(self.fixtures, acquire)

        for file in os.listdir(pdir):
            if file.endswith(self.ftype):
                proc_list = geo_proc(
                    plugin=acquire,
                    src=os.path.join(pdir, file),
                )
                self.assertGreater(len(proc_list), 0, "Product not processed.")

    def test_prism_tmin_early(self) -> None:
        acquire = "prism-tmin-early"
        pdir = os.path.join(self.fixtures, acquire)

        for file in os.listdir(pdir):
            if file.endswith(self.ftype):
                proc_list = geo_proc(
                    plugin=acquire,
                    src=os.path.join(pdir, file),
                )
                self.assertGreater(len(proc_list), 0, "Product not processed.")

    def test_prism_tmin_stable(self) -> None:
        acquire = "prism-tmin-stable"
        pdir = os.path.join(self.fixtures, acquire)

        for file in os.listdir(pdir):
            if file.endswith(self.ftype):
                proc_list = geo_proc(
                    plugin=acquire,
                    src=os.path.join(pdir, file),
                )
                self.assertGreater(len(proc_list), 0, "Product not processed.")

    def test_serfc_qpe_01h(self) -> None:
        acquire = ""

    def test_serfc_qpf_06h(self) -> None:
        acquire = ""

    def test_wpc_qpf_2p5km(self) -> None:
        acquire = "wpc-qpf-2p5km"
        pdir = os.path.join(self.fixtures, acquire)

        for file in os.listdir(pdir):
            if file.endswith(self.ftype):
                proc_list = geo_proc(
                    plugin=acquire,
                    src=os.path.join(pdir, file),
                )
                self.assertGreater(len(proc_list), 0, "Product not processed.")

    def test_wrf_columbia_airtemp(self) -> None:
        acquire = ""

    def test_wrf_columbia_precip(self) -> None:
        acquire = ""


if __name__ == "__main__":
    unittest.main()
