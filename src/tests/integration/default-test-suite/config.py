
# LIMITS includes common repeated reasonability limits for
# testing grid cell values against expected results
LIMITS = {
    'PRECIP_MIN': 0,
    'PRECIP_MAX': 100,
}

# fixture_info includes tuples with pattern (<processor>, <testfile relative path>, <reasonable min>, <reasonable max>)
FIXTURE_INFO = [
    ("abrfc-qpe-01h", "abrfc-qpe-01h/abrfc_qpe_01hr_2022080816Z.nc", LIMITS["PRECIP_MIN"], LIMITS['PRECIP_MAX']),
    ("abrfc-qpe-01h", "abrfc-qpe-02h/abrfc_qpe_01hr_2022080816Z.nc", LIMITS["PRECIP_MIN"], LIMITS['PRECIP_MAX'])
]
