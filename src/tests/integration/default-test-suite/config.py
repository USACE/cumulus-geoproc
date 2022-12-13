from utils import nbm_co_01h_fixture_info_factory

# LIMITS includes common repeated reasonability limits for
# testing grid cell values against expected results
LIMITS = {
    "PRECIP_MIN": 0,
    "PRECIP_MAX": 100,
}
# fmt: off

# Valid date formats that may appear in the filenames
## NOTE: Date without hour is last to accomodate daily products
## Keep it as the last entry.

re_year     = r"(19|20)\d{2}"
re_month    = r"(0[1-9]|1[0-2])"
re_day      = r"(0[1-9]|[1-2][0-9]|3[0-1])"
re_hour     = r"([0-1][0-9]|2[0-3])"
re_minute   = r"([0-5][0-9])"

DATE_FORMATS = [
    ("%Y%m%d%H",    rf"{re_year}{re_month}{re_day}{re_hour}"),
    ("%Y%m%d_%H%M", rf"{re_year}{re_month}{re_day}_{re_hour}{re_minute}"),
    ("%Y_%m_%d_%H", rf"{re_year}_{re_month}_{re_day}_{re_hour}"),
    ("%Y-%m-%d.%H", rf"{re_year}-{re_month}-{re_day}.{re_hour}"),
    ("%Y%m%d-%H",   rf"{re_year}{re_month}{re_day}-{re_hour}"),
    ("%m%d%Y%H",    rf"{re_month}{re_day}{re_year}{re_hour}"), # matches xmrg0809202212z.grb
    ("%Y%m%d",      rf"{re_year}{re_month}{re_day}"),  # KEEP AS LAST ENTRY
]

# fixture_info includes tuples with pattern (<processor>, <testfile relative path>, <reasonable min>, <reasonable max>)
FIXTURE_INFO = [
    ("abrfc-qpe-01h", "abrfc-qpe-01h/abrfc_qpe_01hr_2022080816Z.nc", LIMITS["PRECIP_MIN"], LIMITS['PRECIP_MAX']),
    ("cbrfc-mpe", "cbrfc-mpe/xmrg0809202212z.grb", None, None),
    ("cnrfc-nbm-qpf-06h", "cnrfc-nbm-qpf-06h/QPF.20220822_0700.nc.gz", None, None),
    ("cnrfc-qpf-06h", "cnrfc-qpf-06h/qpf.20221201_1200.nc.gz", None, None),
    ("lmrfc-qpe-01h", "lmrfc-qpe-01h/2022080914z.grib.gz", None, None),
    ("lmrfc-qpf-06h", "lmrfc-qpf-06h/ORN_QPF_SFC_2022080912_234_2022081906f234.grb.gz", None, None),
    ("marfc-fmat-06h", "marfc-fmat-06h/FMAT12hr_20220601.00z.grb", None, None),
    ("marfc-fmat-06h", "marfc-fmat-06h/FMAT12hr_20220601.06z.grb", None, None),
    ("marfc-fmat-06h", "marfc-fmat-06h/FMAT12hr_20220601.12z.grb", None, None),
    ("marfc-fmat-06h", "marfc-fmat-06h/FMAT12hr_20220601.18z.grb", None, None),
    ("marfc-nbmt-01h", "marfc-nbmt-01h/RHA_T_NBM_9hr.2022-08-09.20z.grb", None, None),
    ("marfc-rtmat-01h", "marfc-rtmat-01h/RHA_T_RTMA_1hr.2022-08-09.19z.grb", None, None),
    ("mbrfc-krf-fct-airtemp-01h", "mbrfc-krf-fct-airtemp-01h/krf_hourly_ftemps_grib_2022082501f373.grb.gz", None, None),
    ("mbrfc-krf-qpe-01h", "mbrfc-krf-qpe-01h/krfqpe_2022080921z.grib.gz", None, None),
    ("mbrfc-krf-qpf-06h", "mbrfc-krf-qpf-06h/krf_qpf_grib_2022080918f168.grb.gz", None, None),
    ("naefs-mean-06h", "naefs-mean-06h/NAEFSmean_netcdf2022080912.nc", None, None),
    ("ndfd-conus-airtemp", "ndfd-conus-airtemp/ds.airtemp_202208010054-1-3.bin", None, None),
    ("ndfd-conus-airtemp", "ndfd-conus-airtemp/ds.airtemp_202208010533-4-7.bin", None, None),
    ("ndfd-conus-qpf-06h", "ndfd-conus-qpf-06h/ds.qpf_202208250054.bin", None, None),
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
    ("ncrfc-fmat-01h", "ncrfc-fmat-01h/msr-coe-1hrT--NCRFC_hourlyFcstT_2022022612.tar.gz", None, None),
    ("ncrfc-rtmat-01h", "ncrfc-rtmat-01h/msr-coe-1hrT--NCRFC_RTMA_Obs_1hrT_2022080921z.grb", None, None),
    ("nohrsc-snodas-assimilated", "nohrsc-snodas-assimilated/assim_layers_2022010112.tar", None, None),
    ("nohrsc-snodas-unmasked", "nohrsc-snodas-unmasked/SNODAS_unmasked_20180115.tar", None, None),
    ("prism-ppt-early", "prism-ppt-early/PRISM_ppt_early_4kmD2_20220808_bil.zip", None, None),
    ("prism-ppt-stable", "prism-ppt-stable/PRISM_ppt_stable_4kmD2_19810929_bil.zip", None, None),
    ("prism-tmax-early", "prism-tmax-early/PRISM_tmax_early_4kmD2_20220808_bil.zip", None, None),
    ("prism-tmax-stable", "prism-tmax-stable/PRISM_tmax_stable_4kmD2_19810929_bil.zip", None, None),
    ("prism-tmin-early", "prism-tmin-early/PRISM_tmin_early_4kmD2_20220808_bil.zip", None, None),
    ("prism-tmin-stable", "prism-tmin-stable/PRISM_tmin_stable_4kmD2_19810929_bil.zip", None, None),
    ("serfc-qpe-01h", "serfc-qpe-01h/xmrg0401202200z.grb.gz", None, None),
    ("serfc-qpf-06h", "serfc-qpf-06h/ALR_QPF_SFC_2022040100_006.grb.gz", None, None),
    ("wpc-qpf-2p5km", "wpc-qpf-2p5km/p06m_2022080912f168.grb", None, None),
]

# Append dynamic nbm-co-01h fixtures
FIXTURE_INFO += [
    nbm_co_01h_fixture_info_factory("00", "001"),
    nbm_co_01h_fixture_info_factory("00", "006"),
    nbm_co_01h_fixture_info_factory("01", "001"),
]

# append WRF Columbia
# FIXTURE_INFO += [
#         ("wrf-columbia", "wrf-columbia/DEWPNT_T.nc", None, None),
#         ("wrf-columbia", "wrf-columbia/GROUND_T.nc", None, None),
#         ("wrf-columbia", "wrf-columbia/LWDOWN__.nc", None, None),
#         ("wrf-columbia", "wrf-columbia/PRECIPAH.nc", None, None),
#         ("wrf-columbia", "wrf-columbia/PSTARCRS.nc", None, None),
#         ("wrf-columbia", "wrf-columbia/RH______.nc", None, None),
#         ("wrf-columbia", "wrf-columbia/SWDOWN__.nc", None, None),
#         ("wrf-columbia", "wrf-columbia/T2______.nc", None, None),
#         ("wrf-columbia", "wrf-columbia/U10_____.nc", None, None),
#         ("wrf-columbia", "wrf-columbia/V10_____.nc", None, None),
#         ("wrf-columbia", "wrf-columbia/VAPOR_PS.nc", None, None),
#     ]

# append WRF British Columbia
# FIXTURE_INFO+=[
#         ("wrf-bc", "wrf-bc/DEWPNT_T.nc", None, None),
#         ("wrf-bc", "wrf-bc/GROUND_T.nc", None, None),
#         ("wrf-bc", "wrf-bc/LWDOWN__.nc", None, None),
#         ("wrf-bc", "wrf-bc/PRECIPAH.nc", None, None),
#         ("wrf-bc", "wrf-bc/PSTARCRS.nc", None, None),
#         ("wrf-bc", "wrf-bc/RH______.nc", None, None),
#         ("wrf-bc", "wrf-bc/SWDOWN__.nc", None, None),
#         ("wrf-bc", "wrf-bc/T2______.nc", None, None),
#         ("wrf-bc", "wrf-bc/U10_____.nc", None, None),
#         ("wrf-bc", "wrf-bc/V10_____.nc", None, None),
#         ("wrf-bc", "wrf-bc/VAPOR_PS.nc", None, None),
#     ]

# fmt: on
