import pandas as pd


rename = {
    'MCAID_PROB1': 'MEDICAID_PROB1',
    'MCAID_PROB10': 'MEDICAID_PROB10',
    'MCAID_PROB11': 'MEDICAID_PROB11',
    'MCAID_PROB12': 'MEDICAID_PROB12',
    'MCAID_PROB13': 'MEDICAID_PROB13',
    'MCAID_PROB14': 'MEDICAID_PROB14',
    'MCAID_PROB15': 'MEDICAID_PROB15',
    'MCAID_PROB2': 'MEDICAID_PROB2',
    'MCAID_PROB3': 'MEDICAID_PROB3',
    'MCAID_PROB4': 'MEDICAID_PROB4',
    'MCAID_PROB5': 'MEDICAID_PROB5',
    'MCAID_PROB6': 'MEDICAID_PROB6',
    'MCAID_PROB7': 'MEDICAID_PROB7',
    'MCAID_PROB8': 'MEDICAID_PROB8',
    'MCAID_PROB9': 'MEDICAID_PROB9',
    'MCAID_VAL1': 'MEDICAID_VAL1',
    'MCAID_VAL10': 'MEDICAID_VAL10',
    'MCAID_VAL11': 'MEDICAID_VAL11',
    'MCAID_VAL12': 'MEDICAID_VAL12',
    'MCAID_VAL13': 'MEDICAID_VAL13',
    'MCAID_VAL14': 'MEDICAID_VAL14',
    'MCAID_VAL15': 'MEDICAID_VAL15',
    'MCAID_VAL2': 'MEDICAID_VAL2',
    'MCAID_VAL3': 'MEDICAID_VAL3',
    'MCAID_VAL4': 'MEDICAID_VAL4',
    'MCAID_VAL5': 'MEDICAID_VAL5',
    'MCAID_VAL6': 'MEDICAID_VAL6',
    'MCAID_VAL7': 'MEDICAID_VAL7',
    'MCAID_VAL8': 'MEDICAID_VAL8',
    'MCAID_VAL9': 'MEDICAID_VAL9',
    'MCARE_PROB1': 'MEDICARE_PROB1',
    'MCARE_PROB10': 'MEDICARE_PROB10',
    'MCARE_PROB11': 'MEDICARE_PROB11',
    'MCARE_PROB12': 'MEDICARE_PROB12',
    'MCARE_PROB13': 'MEDICARE_PROB13',
    'MCARE_PROB14': 'MEDICARE_PROB14',
    'MCARE_PROB15': 'MEDICARE_PROB15',
    'MCARE_PROB2': 'MEDICARE_PROB2',
    'MCARE_PROB3': 'MEDICARE_PROB3',
    'MCARE_PROB4': 'MEDICARE_PROB4',
    'MCARE_PROB5': 'MEDICARE_PROB5',
    'MCARE_PROB6': 'MEDICARE_PROB6',
    'MCARE_PROB7': 'MEDICARE_PROB7',
    'MCARE_PROB8': 'MEDICARE_PROB8',
    'MCARE_PROB9': 'MEDICARE_PROB9',
    'MCARE_VAL1': 'MEDICARE_VAL1',
    'MCARE_VAL10': 'MEDICARE_VAL10',
    'MCARE_VAL11': 'MEDICARE_VAL11',
    'MCARE_VAL12': 'MEDICARE_VAL12',
    'MCARE_VAL13': 'MEDICARE_VAL13',
    'MCARE_VAL14': 'MEDICARE_VAL14',
    'MCARE_VAL15': 'MEDICARE_VAL15',
    'MCARE_VAL2': 'MEDICARE_VAL2',
    'MCARE_VAL3': 'MEDICARE_VAL3',
    'MCARE_VAL4': 'MEDICARE_VAL4',
    'MCARE_VAL5': 'MEDICARE_VAL5',
    'MCARE_VAL6': 'MEDICARE_VAL6',
    'MCARE_VAL7': 'MEDICARE_VAL7',
    'MCARE_VAL8': 'MEDICARE_VAL8',
    'MCARE_VAL9': 'MEDICARE_VAL9',

    'VET_PROB1': 'VB_PROB1',
    'VET_PROB10': 'VB_PROB10',
    'VET_PROB11': 'VB_PROB11',
    'VET_PROB12': 'VB_PROB12',
    'VET_PROB13': 'VB_PROB13',
    'VET_PROB14': 'VB_PROB14',
    'VET_PROB15': 'VB_PROB15',
    'VET_PROB2': 'VB_PROB2',
    'VET_PROB3': 'VB_PROB3',
    'VET_PROB4': 'VB_PROB4',
    'VET_PROB5': 'VB_PROB5',
    'VET_PROB6': 'VB_PROB6',
    'VET_PROB7': 'VB_PROB7',
    'VET_PROB8': 'VB_PROB8',
    'VET_PROB9': 'VB_PROB9',
    'VET_VAL1': 'VB_VAL1',
    'VET_VAL10': 'VB_VAL10',
    'VET_VAL11': 'VB_VAL11',
    'VET_VAL12': 'VB_VAL12',
    'VET_VAL13': 'VB_VAL13',
    'VET_VAL14': 'VB_VAL14',
    'VET_VAL15': 'VB_VAL15',
    'VET_VAL2': 'VB_VAL2',
    'VET_VAL3': 'VB_VAL3',
    'VET_VAL4': 'VB_VAL4',
    'VET_VAL5': 'VB_VAL5',
    'VET_VAL6': 'VB_VAL6',
    'VET_VAL7': 'VB_VAL7',
    'VET_VAL8': 'VB_VAL8',
    'VET_VAL9': 'VB_VAL9'
}
rename_lower = {
    'SSI': 'ssi',
    'VB': 'vet',
    'SNAP': 'snap',
    'MEDICARE': 'mcare',
    'MEDICAID': 'mcaid',
    'WIC': 'wic',
    'TANF': 'tanf',
    'HOUSING': 'housing'
}

rev_rename = {rename[k]: k for k in rename}
rev_rename.update(rename_lower)
cps = pd.read_csv('../cps_data/cps_raw.csv.gz', compression="gzip")
cps.rename(columns=rev_rename, inplace=True)
cps['housing'] *= 12
cps.to_csv('../cps_data/cps_raw_rename.csv.gz', compression="gzip")
