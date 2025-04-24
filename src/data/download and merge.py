
import pandas as pd
import requests
import io
import logging
import os
import pandas as pd

url_macro = 'https://github.com/KMueller-Lab/Global-Macro-Database/raw/refs/heads/main/data/final/chainlinked_infl.dta'
df_macro = pd.read_stata(url_macro)

print(df_macro.columns)
#url_oecd = "https://sdmx.oecd.org/public/rest/data/OECD.SDD.TPS,DSD_PDB@DF_PDB_ULC_Q,1.0/.Q.......?startPeriod=1990-Q4&format=csv"
# Fetch data from the URL
#df_oecd = pd.read_csv(url_oecd)
#print(df_oecd.columns)


# Load the .dta file into a pandas DataFrame
url = 'https://github.com/KMueller-Lab/Global-Macro-Database/raw/refs/heads/main/data/final/chainlinked_rGDP.dta'
df_rGDP = pd.read_stata(url)

# Check the first few rows to understand the structure
print(df_rGDP.columns)
