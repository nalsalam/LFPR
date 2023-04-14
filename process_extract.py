
# import numpy as np
# import pandas as pd
# from ipumspy import readers

import CPSprocessPy as z

# If you have module ipumspy you can uncomment the next line
# cps_raw = z.read_cps_extract("cps_00188")

# For those without the ipumspy module I have saved a 1k sample of cps_raw using this:
# pd.to_pickle(cps_raw.sample(n = 1000), "data/cps_raw_1k.pkl")
from pandas import read_pickle
cps_raw = read_pickle("data/cps_raw_1k.pkl")

cps_raw.info()

cps = cps_raw.copy()

cps = z.mod_sex(cps)
cps = z.add_agecat15(cps)
cps = z.add_race_eth(cps)
cps = z.add_edcat(cps)
cps = z.edit_edcat(cps)

# add a column with quarter
cps["quarter"] = 1 + (cps.month - 1) % 3

# filter out military
cps = cps[cps.empstat != 1]

cps.info()

# save for easy inspection in next step
from pandas import to_pickle
to_pickle(cps, "data/cps.pkl")

