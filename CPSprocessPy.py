

# https://www.section.io/engineering-education/how-to-store-your-python-functions-into-modules/

# the environment of a function is determined at the time it is created not when run
# so need to import the functions here or
# inside the function

import numpy as np
import pandas as pd

def read_cps_extract(extract_file):
    """
    """
    from ipumspy import (IpumsApiClient, 
                        UsaExtract,
                        readers, 
                        save_extract_as_json,
                        define_extract_from_json,
                        define_extract_from_ddi)

    cps_raw_ddi = readers.read_ipums_ddi(f'{extract_file}.xml')
    cps_raw = readers.read_microdata(cps_raw_ddi, f'{extract_file}.dat.gz')

    # drop unneeded series
    cps_raw.drop(columns = ['HWTFINL', 'CPSID', 'ASECFLAG'], inplace = True)

    # lower case column names
    cps_raw.columns = cps_raw.columns.str.lower()

    return cps_raw

def mod_sex(cps):
    """Modifies integer "sex" to be a categorical variable with labels

    Args:
        cps (dataframe): with a 1/2 integer variable indicating sex

    Returns:
        dataframe: with the new sex categorical variable
    """
    cps["sex"] = np.where(cps["sex"] == 1, "Men", "Women")
    return cps

# create agecat15
def add_agecat15(cps):
    """
    kids are present, no na's
    """
    age_breaks = [0, 16, 18, 20, 25, 30, 35, 40, 45, 50, 55, 60, 62, 65, 70, 80, 91]
    age_labels = ["0-15", "16-17", "18-19", "20-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50-54", "55-59", "60-61", "62-64", "65-69", "70-79", "80+"]
    cps["agecat15"] = pd.cut(cps.age, age_breaks, right = False, ordered = True, labels = age_labels)
    return cps

# To avoid this error:
# TypeError: invalid entry 0 in condlist: should be boolean ndarray
# I added "astype(bool)" to each condition.
# https://stackoverflow.com/questions/68618078/invalid-entry-0-in-condlist-should-be-boolean-ndarray-using-np-select

def add_race_eth(cps):
    conditions = [
        (cps["hispan"].ne(0)).astype(bool),
        (cps["race"].isin([200, 801, 805, 806, 807, 810, 811, 814, 816, 818, 830])).astype(bool),
        (cps["race"].eq(100)).astype(bool)
        ]
    choices = (["Hispanic", "Black", "White"])
    cps["race_eth"] = np.select(conditions, choices, default = "Asian and Other")
    return cps

def add_edcat(cps):
    """
    edcat
    """

    conditions = [
        ((cps["year"] >= 1992) & (cps["educ"] <= 71)).astype(bool),
        ((cps["year"] >= 1992) & (cps["educ"] == 73)).astype(bool),
        ((cps["year"] >= 1992) & (cps["educ"].isin([81, 91, 92]))).astype(bool),
        ((cps["year"] >= 1992) & (cps["educ"] == 111)).astype(bool),
        ((cps["year"] >= 1992) & (cps["educ"].isin([123, 124, 125]))).astype(bool)
        ]
        # Pre-1992
        # higrade <= 141 ~ 1, # some 12th, did not finish
        # higrade == 150 ~ 2, # finished 12th grade
        # higrade <= 181 ~ 3, # some 4th, didn't finish down to some first didn't finish
        # higrade <= 200 ~ 4, # includes 5th year ... smooths transition of edcat 4 & 5
        # higrade <= 210 ~ 5, # 6th year not finished or more
        # TRUE ~ NA_real_
        
    choices = [1, 2, 3, 4, 5]
    cps["edcat"] = np.select(conditions, choices)
    return cps

def edit_edcat(cps):
    """
    When multiple conditions are satisfied, the first one encountered in condlist is used.
    """
    conditions = [
        (cps["age"] <= 15).astype(bool),
        (cps["age"].isin([16, 17])).astype(bool),
        ((cps["age"].isin([18, 19])) & (cps["edcat"].isin([3, 4, 5]))).astype(bool),
        ((cps["age"].isin(range(20, 25))) & (cps["edcat"] == 5)).astype(bool),
        ((cps["age"].isin(range(70, 81))) & (cps["edcat"] == 5) & (cps["race_eth"] == "Black")).astype(bool),
        ((cps["age"].isin(range(70, 90))) & (cps["edcat"].isin([4, 5])) & (cps["race_eth"].isin(["Hispanic", "Asian and Other"]))).astype(bool)
    ]
    choices = [None, 1, 2, 4, 4, 3]
    cps["edcat"] = np.select(conditions, choices, default = cps["edcat"])
    return cps


