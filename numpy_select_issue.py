import numpy as np
import pandas as pd

# a random subset of 1000
cps = pd.read_pickle("data/cps_1k.pkl") 

conditions = [(cps["hispan"] != 0), (cps["hispan"] == 0)]
choices = [False, True]
# TypeError
# cps["is_hispanic"] = np.select(conditions, choices)

# Works
conditions = [(cps["hispan"] != 0).astype(bool), (cps["hispan"] == 0).astype(bool)]
cps["is_hispanic"] = np.select(conditions, choices)
cps["is_hispanic"] = np.select(conditions, choices)