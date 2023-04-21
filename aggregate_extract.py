import pandas as pd
import numpy as np

cps = pd.read_pickle("data/cps.pkl")

# sums up wtfinl, leaves the name unchanged
# pop_asre = cps.groupby(['agecat15', 'sex', 'race_eth', 'edcat'])['wtfinl'].sum()

def sum_millions(wtfinl):
    return sum(wtfinl) / 1e6

# sums up wtfinl and divides by 1e6
# pop_asre = cps.groupby(['agecat15', 'sex', 'race_eth', 'edcat'])['wtfinl'].agg(sum_millions)

# changes the name to pop
pop_asre = cps.groupby(['agecat15', 'sex', 'race_eth', 'edcat']).agg(pop = ('wtfinl', sum_millions))

