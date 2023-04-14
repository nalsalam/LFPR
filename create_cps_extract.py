
import sys
import os

import pandas as pd
import numpy as np
from datetime import date, datetime, timedelta

# Earlier ipumspy has been installed with, for example, pip install ipumspy
from ipumspy import (IpumsApiClient, 
                     CpsExtract,
                     readers, 
                     save_extract_as_json,
                     define_extract_from_json,
                     define_extract_from_ddi)

# create a list with the desired samples
ids = pd.read_csv("data/cps_samples.csv")

ids["year"] = ids.sample_id.str[3:7].astype(int)
ids["month"] = ids.sample_id.str[8:10].astype(int)
ids["asec"] = ids.sample_id.str[8:11] == "03s" 

cr_date = lambda row : date(row["year"], row["month"], 1)
ids["date"] = ids.apply(cr_date, axis = 1)

samples = ids[(ids.date > date(2020, 2, 15))][ids.asec == False].sample_id

with open(".env", "r") as file:
    my_api_key = file.readline().split("=")[1].rstrip("\n") 
ipums = IpumsApiClient(my_api_key)

extract = CpsExtract(samples,
                     # YEAR, MONTH, WTFINL, SERIAL, PERNUM, CPSIDP, HWTFINL, CPSID automatically added
                     ["EMPSTAT", "AGE", "SEX", "EDUC", "RACE", "HISPAN", "MARST", "NCHLT5"],
                     description="CPS Extract for LFPR Modelling.")

ipums.submit_extract(extract)
ipums.extract_status(extract)

ipums.wait_for_extract(extract)
print(f"{extract.collection} number {extract.extract_id} is complete!")
ipums.download_extract(extract)
