import pandas as pd
import numpy as np

cps = pd.read_pickle("data/cps.pkl")

# pop_asre = cps.groupby(['agecat15', 'sex', 'race_eth', 'edcat'])['wtfinl'].sum()

def sum_millions(wtfinl):
    return sum(wtfinl) / 1e6

# pop_asre = cps.groupby(['agecat15', 'sex', 'race_eth', 'edcat'])['wtfinl'].agg(sum_millions)

pop_asre = cps.groupby(['agecat15', 'sex', 'race_eth', 'edcat']).agg(pop = ('wtfinl', sum_millions))

