
# The code in this file is meant to be run interactively

import pandas as pd
import numpy as np
cps = pd.read_pickle("data/cps.pkl")

# kids have NaNs
cps.edcat.value_counts(sort = False, dropna = False).sort_index()

# young people constrained to have less education
# kids are na and don't appear
pd.crosstab(index = cps.agecat15, columns = cps.edcat)
pd.pivot_table(cps, values = 'wtfinl', index = 'agecat15', columns = 'edcat', aggfunc = np.sum, dropna = False)

# selector operator [] is the primary way of filtering (subsetting) a dataframe
cps[cps["agecat15"].ge("25-29")].agecat15.value_counts().sort_index()
cps[cps["agecat15"] >= "25-29"].agecat15.value_counts().sort_index()

# query is another way to filter (subset) a dataframe
# seems to use tidy eval
cps.query('sex == "Men"').sex.value_counts().sort_index()
cps.query('edcat >= 3').edcat.value_counts().sort_index()
cps.query('agecat15.ge("25-29")').agecat15.value_counts().sort_index() # >= raises ValueError

# In CPSprocessPy.py I used numpy where and numpy select to create category variables
# Here are two other ways using base python replace and map
# numpy select is clearly the faster than replace and map

cps["empstat"].value_counts().sort_index()

cps["lfstat"] = cps["empstat"].astype(str).replace(["0", "10", "12", "21", "22", "32", "34", "36"], [None, "E", "E", "U", "U", "N", "N", "N"]).astype('category')
cps.lfstat.value_counts(dropna = False)

cps["lfstat"] = cps["empstat"].astype(str).map({"0": None, "10" : "E", "12" : "E", "21" : "U", "22" : "U", "32" : "N", "34" : "N", "36" : "N"}).astype('category')
cps.lfstat.value_counts(dropna = False)

conditions = [cps.empstat.isin([10, 12]).astype(bool),
              cps.empstat.isin([21, 22]).astype(bool),
              cps.empstat.isin([32, 34, 36]).astype(bool),
              True]
choices = ["E", "U", "N", None]
cps["lfstat"] = np.select(conditions, choices)
cps.lfstat.value_counts(dropna = False)
                           

