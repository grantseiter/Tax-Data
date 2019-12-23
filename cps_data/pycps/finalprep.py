"""
Clean up the CPS file and make it ready for Tax-Calculator
"""
import numpy as np
import pandas as pd


def drop_vars(data):
    """
    Returns Pandas DataFrame of data without unuseable variables
    """
    USEABLE_VARS = {
        'DSI', 'EIC', 'FLPDYR', 'MARS', 'MIDR', 'RECID', 'XTOT', 'age_head',
        'age_spouse', 'agi_bin', 'blind_head', 'blind_spouse', 'cmbtp',
        'e00200', 'e00200p', 'e00200s', 'e00300', 'e00400', 'e00600', 'e00650',
        'e00700', 'e00800', 'e00900', 'e00900p', 'e00900s', 'e01100', 'e01200',
        'e01400', 'e01500', 'e01700', 'e02000', 'e02100', 'e02100p', 'e02100s',
        'e02300', 'e02400', 'e03150', 'e03220', 'e03230', 'e03240', 'e03270',
        'e03290', 'e03300', 'e03400', 'e03500', 'e07240', 'e07260', 'e07300',
        'e07400', 'e07600', 'e09700', 'e09800', 'e09900', 'e11200', 'e17500',
        'e18400', 'e18500', 'e19200', 'e19800', 'e20100', 'e20400', 'g20500',
        'e24515', 'e24518', 'e26270', 'e27200', 'e32800', 'e58990', 'e62900',
        'e87530', 'elderly_dependents', 'f2441', 'f6251', 'n24',
        'nu05', 'nu13', 'nu18', 'n1820', 'n21', 'p08000', 'p22250', 'p23250',
        'p25470', 'p87521', 's006', 'e03210', 'ssi_ben', 'snap_ben',
        'vet_ben', 'mcare_ben', 'mcaid_ben', 'oasdi_ben', 'other_ben',
        'h_seq', 'ffpos', 'fips', 'a_lineno', 'tanf_ben', 'wic_ben',
        'housing_ben', "linenos"
    }

    drop_vars = list(set(data.columns) - USEABLE_VARS)
    data = data.drop(drop_vars, axis=1)

    return data


def add_agi_bin(data, col_name):
    """
    Add an AGI bin indicator used in Tax-Calc to apply adjustment factors
    """
    THRESHOLDS_K = [-np.inf, 0, 5, 10, 15, 20, 25, 30, 40, 50, 75, 100, 200,
                    500, 1000, 1500, 2000, 5000, 10000, np.inf]
    thresholds = [x * 1000 for x in THRESHOLDS_K]
    data['agi_bin'] = pd.cut(data[col_name], thresholds,
                             labels=np.arange(0, len(THRESHOLDS_K) - 1),
                             right=False)

    return data


def deduction_limits(data):
    """
    Apply limits on itemized deductions
    """
    # Split charitable contributions into cash and non-cash using ratio in PUF
    cash = 0.82013
    non_cash = 1. - cash
    data['e19800'] = data['CHARITABLE'] * cash
    data['e20100'] = data['CHARITABLE'] * non_cash

    # Apply student loan interest deduction limit
    data['e03210'] = np.where(data["SLINT"] > 2500, 2500, data["SLINT"])

    # Apply IRA contribution limit
    deductable_ira = np.where(
        data["age_head"] >= 50,
        np.where(data["ADJIRA"] > 6500, 6500, data["ADJIRA"]),
        np.where(data["ADJIRA"] > 5500, 5500, data["ADJIRA"])
    )
    data['e03150'] = deductable_ira

    return data


def final_prep(data):
    """
    Function for cleaning up the CPS file
    """
    # recode blind variables
    data["blind_head"] = np.where(
        data["blind_head"] == 1, 1, 0
    )
    data["blind_spouse"] = np.where(
        data["blind_spouse"] == 1, 1, 0
    )

    # cap EIC
    data["EIC"] = np.minimum(data["EIC"], 3)

    # apply deduction deduction
    data = deduction_limits(data)

    # rename variables
    RENAMES = {
        "mars": "MARS",
        "dep_stat": "DSI",
        "divs": "e00600",
        "CGAGIX": "e01100",
        "DPAD": "e03240",
        "TIRAD": "e01400",
        "SLINT": "e18400",
        "SEHEALTH": "e03270",
        "KEOGH": "e03300",
        "MEDEX": "e17500"
    }
    data = data.rename(columns=RENAMES)

    # add record ID
    data["RECID"] = range(1, len(data.index) + 1)

    # add AGI bins
    data = add_agi_bin(data, "agi")
    data = drop_vars(data)
    # clean data
    data = data.fillna(0.)
    data = data.astype(np.int32)
    data['e00200'] = data['e00200p'] + data['e00200s']
    data['e00900'] = data['e00900p'] + data['e00900s']
    data['e02100'] = data['e02100p'] + data['e02100s']
    data['e00650'] = np.minimum(data['e00600'], data['e00650'])
    data['s006'] *= 100

    return data


if __name__ == "__main__":
    data = pd.read_csv("cps_raw.csv.gz")
    data = final_prep(data)
    data.to_csv("cps.csv.gz", index=None, compression="gzip")
