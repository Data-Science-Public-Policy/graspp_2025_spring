
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


#url_oecd = "https://sdmx.oecd.org/public/rest/data/OECD.SDD.TPS,DSD_PDB@DF_PDB_ULC_Q,1.0/.Q.......?startPeriod=1990-Q4&format=csv"
#response = requests.get(url_oecd)
#response.raise_for_status()  # Raise an exception for HTTP errors
# Read the text data into an in-memory text buffer
#data = io.StringIO(response.text)
# Read CSV data into a pandas DataFrame
#df_oecd = pd.read_csv(data)

#print(df_oecd.columns)



url = "https://sdmx.oecd.org/public/rest/data/OECD.SDD.NAD,DSD_NAMAIN1@DF_QNA_BY_ACTIVITY_COE,1.1/Q..AUT..........?startPeriod=2023-Q4&dimensionAtObservation=AllDimensions&format=csv"

response = requests.get(url)
response.raise_for_status()

data = io.StringIO(response.text)
df = pd.read_csv(data)

print(df.head(10))
print(df['OBS_VALUE'])



