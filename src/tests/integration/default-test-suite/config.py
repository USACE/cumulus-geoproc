from utils import nbm_co_01h_fixture_info_factory

# LIMITS includes common repeated reasonability limits for
# testing grid cell values against expected results
LIMITS = {
    "PRECIP_MIN": 0,
    "PRECIP_MAX": 100,
}

# Valid date formats that may appear in the filenames
# Date without hour is last to accomodate daily products
DATE_FORMATS = [
    ("%Y%m%d%H", r"\d{4}\d{2}\d{2}\d{2}"),
    ("%Y%m%d_%H%M", r"\d{4}\d{2}\d{2}_\d{4}"),
    ("%Y-%m-%d.%H", r"\d{4}-\d{2}-\d{2}\.\d{2}"),
    ("%Y%m%d-%H", r"\d{4}\d{2}\d{2}-\d{2}"),
    ("%Y%m%d", r"\d{4}\d{2}\d{2}"),
]

# fmt: off
# fixture_info includes tuples with pattern (<processor>, <testfile relative path>, <reasonable min>, <reasonable max>)
FIXTURE_INFO = [
    ("abrfc-qpe-01h", "abrfc-qpe-01h/abrfc_qpe_01hr_2022080816Z.nc", LIMITS["PRECIP_MIN"], LIMITS['PRECIP_MAX']),
    ("cbrfc-mpe", "cbrfc-mpe/xmrg0809202212z.grb", None, None),
    ("cnrfc-qpe-06h", "cnrfc-qpe-06h/qpe.20220803_1200.nc.gz", None, None),
    ("lmrfc-qpe-01h", "lmrfc-qpe-01h/2022080914z.grib.gz", None, None),
    ("lmrfc-qpf-06h", "lmrfc-qpf-06h/ORN_QPF_SFC_2022080912_234_2022081906f234.grb.gz", None, None),
    ("marfc-nbmt-01h", "marfc-nbmt-01h/RHA_T_NBM_9hr.2022-08-09.20z.grb", None, None),
    ("marfc-rtmat-01h", "marfc-rtmat-01h/RHA_T_RTMA_1hr.2022-08-09.19z.grb", None, None),
    ("mbrfc-krf-fct-airtemp-01h", "mbrfc-krf-fct-airtemp-01h/krf_hourly_ftemps_grib_2022082501f373.grb.gz", None, None),
    ("mbrfc-krf-qpe-01h", "mbrfc-krf-qpe-01h/krfqpe_2022080921z.grib.gz", None, None),
    ("mbrfc-krf-qpf-06h", "mbrfc-krf-qpf-06h/krf_qpf_grib_2022080918f168.grb.gz", None, None),
    ("naefs-mean-06h", "naefs-mean-06h/NAEFSmean_netcdf2022080912.nc", None, None),
    ("ncep-mrms-v12-msqpe01h-p1-alaska","ncep-mrms-v12-msqpe01h-p1-alaska/MRMS_MultiSensor_QPE_01H_Pass1_00.00_20220809-150000.grib2.gz", None, None),
    ("ncep-mrms-v12-msqpe01h-p1-carib", "ncep-mrms-v12-msqpe01h-p1-carib/MRMS_MultiSensor_QPE_01H_Pass1_00.00_20220809-150000.grib2.gz", None, None),
    ("ncep-mrms-v12-msqpe01h-p2-alaska", "ncep-mrms-v12-msqpe01h-p2-alaska/MRMS_MultiSensor_QPE_01H_Pass2_00.00_20220809-150000.grib2.gz", None, None),
    ("ncep-mrms-v12-msqpe01h-p2-carib", "ncep-mrms-v12-msqpe01h-p2-carib/MRMS_MultiSensor_QPE_01H_Pass2_00.00_20220809-150000.grib2.gz", None, None),
    ("ncep-mrms-v12-multisensor-qpe-01h-pass1", "ncep-mrms-v12-multisensor-qpe-01h-pass1/MRMS_MultiSensor_QPE_01H_Pass1_00.00_20220809-150000.grib2.gz", None, None),
    ("ncep-mrms-v12-multisensor-qpe-01h-pass2", "ncep-mrms-v12-multisensor-qpe-01h-pass2/MRMS_MultiSensor_QPE_01H_Pass2_00.00_20220809-150000.grib2.gz", None, None),
    ("ncep-stage4-mosaic-01h", "ncep-stage4-mosaic-01h/st4_conus.2022081004.01h.grb2", None, None),
    ("ncep-stage4-mosaic-06h", "ncep-stage4-mosaic-06h/st4_conus.2022080718.06h.grb2", None, None),
    ("ncep-stage4-mosaic-24h", "ncep-stage4-mosaic-24h/st4_conus.2022080512.24h.grb2", None, None),
    ("ncrfc-mpe-01h", "ncrfc-mpe-01h/MSR_mpe-lx_2022080922z.grb", None, None),
    ("ncrfc-rtmat-01h", "ncrfc-rtmat-01h/msr-coe-1hrT--NCRFC_RTMA_Obs_1hrT_2022080921z.grb", None, None),
    ("nohrsc-snodas-unmasked", "nohrsc-snodas-unmasked/SNODAS_unmasked_20180115.tar", None, None),
    ("prism-ppt-early", "prism-ppt-early/PRISM_ppt_early_4kmD2_20220808_bil.zip", None, None),
    ("prism-ppt-stable", "prism-ppt-stable/PRISM_ppt_stable_4kmD2_19810929_bil.zip", None, None),
    ("prism-tmax-early", "prism-tmax-early/PRISM_tmax_early_4kmD2_20220808_bil.zip", None, None),
    ("prism-tmax-stable", "prism-tmax-stable/PRISM_tmax_stable_4kmD2_19810929_bil.zip", None, None),
    ("prism-tmin-early", "prism-tmin-early/PRISM_tmin_early_4kmD2_20220808_bil.zip", None, None),
    ("prism-tmin-stable", "prism-tmin-stable/PRISM_tmin_stable_4kmD2_19810929_bil.zip", None, None),
    ("wpc-qpf-2p5km", "wpc-qpf-2p5km/p06m_2022080912f168.grb", None, None),
]

# Append dynamic nbm-co-01h fixtures
FIXTURE_INFO += [
    nbm_co_01h_fixture_info_factory("00", "001"),
]
# fmt: on
