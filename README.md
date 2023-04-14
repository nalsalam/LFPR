# LFPR
Labor Force Participation Rates By Demographic Group Based on the IPUMS CPS

Using ipumspy to create an extract from IPUMS and python pandas and numpy to process the extract.

As a part of the processing, we create:

+ agecat15, a category variable from age cut into 15 ranges and labelled

+ sex, a category variable labelled "Men" and "Women"

+ race_eth, a combination of race and Hispanic ethnicity in four groups

+ edcat, educational attainment in 5 ranges

+ lfstat, employment status reduced to three categories: employed, unemployed, not-in-labor-force (TBD. Code that works is in inspect_extract.py)

Finally, an aggregated dataset with population by year, agecat15, sex, race_eth, and edcat. (TBD)

If you don't ipumspy package installed, the repo includes a 1000 random subsample.  Start with process_extract.py and run it. Then run the code in inspect_extract.py interactively.

If you have the ipumspy package installed, you can start with running create_cps_extract.py.  Then uncomment/comment out a few lines at the top of process_extract.py to use the extracts instead of the small sample mentioned above and run it.  Finally, run the code in inspect_extract.py interactively.




