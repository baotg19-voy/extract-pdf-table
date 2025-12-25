"""Column mappings for allowance PDF layouts"""

# 37-column mapping (compact structure)
COLUMNS_37 = [
    'untenshu', 'sagawa_a', 'sagawa_b', 'sagawa_ba', 'sagawa_bb', 'sagawa_bba', 
    'sagawa_bbb', 'sagawa_bbba', 'rinji_teate', 'chokyori_teate', 'joshu',
    'ippan_a', 'ippan_b', 'ippan_ba', 'ippan_bb', 'ippan_bba', 'ippan_bbb',
    'yontonsha_a', 'yontonsha_b', 'yontonsha_ba', 'yontonsha_bb', 'yontonsha_bba',
    'yontonsha_bbb', 'yontonsha_bbba', 'sagawa_ippan_b', 'sagawa_ippan_ba',
    'sagawa_ippan_bb', 'sagawa_ippan_bba', 'juyon_yonhei_b', 'juyon_yonhei_ba',
    'juyon_yonhei_bb', 'juronton_yontonhei_bba', 'lorry_a', 'lorry_b',
    'lorry_ba', 'lorry_bb', 'gokei'
]

# 44-column mapping (with spacing columns)
COLUMNS_44 = [
    'untenshu', 'sagawa_a', 'sagawa_b', 'sagawa_ba', 'sagawa_bb', 'sagawa_bba',
    'sagawa_bbb', 'sagawa_bbba', 'rinji_teate', 'chokyori_teate', 'joshu',
    'ippan_a', 'ippan_b', 'ippan_b', 'ippan_ba', 'ippan_ba', 'ippan_bb',
    'ippan_bb', 'ippan_bba', 'ippan_bbb', 'yontonsha_a', 'yontonsha_b',
    'yontonsha_b', 'yontonsha_ba', 'yontonsha_ba', 'yontonsha_bb', 'yontonsha_bba',
    'yontonsha_bbb', 'yontonsha_bbba', 'sagawa_ippan_b', 'sagawa_ippan_ba',
    'sagawa_ippan_bb', 'sagawa_ippan_bba', 'juyon_yonhei_b', 'juyon_yonhei_ba',
    'juyon_yonhei_bb', 'juronton_yontonhei_bba', 'lorry_a', 'lorry_b',
    'lorry_b', 'lorry_ba', 'lorry_ba', 'lorry_bb', 'gokei'
]


def get_columns(num_cols):
    """Get column mapping for table width"""
    if num_cols == 37:
        return COLUMNS_37
    elif num_cols == 44:
        return COLUMNS_44
    else:
        # Best fit
        return COLUMNS_37[:num_cols] if num_cols <= 37 else COLUMNS_44[:num_cols]
