import pandas as pd
import requests
import io
import os

### 1. Download Data ###
# Define URL for macroeconomic data
url_macro = 'https://github.com/KMueller-Lab/Global-Macro-Database/raw/refs/heads/main/data/final/chainlinked_rGDP.dta'
# Read Stata file into a pandas DataFrame
df_macro = pd.read_stata(url_macro)

# Define URL for OECD data
url_oecd = "https://sdmx.oecd.org/public/rest/data/OECD.SDD.TPS,DSD_PDB@DF_PDB_ULC_Q,1.0/.Q.......?startPeriod=1990-Q4&format=csv"
# Fetch data from the URL
response = requests.get(url_oecd)
response.raise_for_status()  # Raise an exception for HTTP errors
# Read the text data into an in-memory text buffer
data = io.StringIO(response.text)
# Read CSV data into a pandas DataFrame
df_oecd = pd.read_csv(data)

### 2. Filter and Rename Columns ###
# Filter macroeconomic data for Japan, select columns, and drop missing values
df_macro_jp = df_macro.query("ISO3 == 'JPN'")[['ISO3', 'year', 'UN_rGDP', 'WDI_rGDP']].dropna()
# Filter OECD data for Japan and specific measures/units
df_oecd_jp = df_oecd[['REF_AREA', 'TIME_PERIOD', 'OBS_VALUE', 'MEASURE', 'UNIT_MEASURE']].query("REF_AREA == 'JPN' & MEASURE=='ULCE' & UNIT_MEASURE == 'PA'")

# Rename columns in the Japan macroeconomic DataFrame
df_macro_jp = df_macro_jp.rename({"ISO3":'country', "year":'date'}, axis=1)

# Rename columns and drop unnecessary columns in the Japan OECD DataFrame
df_oecd_jp = df_oecd_jp.rename({"REF_AREA":'country', "TIME_PERIOD":'date', 'OBS_VALUE':'ULCE'}, axis=1).drop(["MEASURE", "UNIT_MEASURE"], axis=1)

### 3. Datetime Conversion ###
## Convert the 'date' column in the OECD DataFrame to datetime objects from quarterly periods and then to date
df_oecd_jp['date'] = pd.PeriodIndex(df_oecd_jp['date'], freq='Q').to_timestamp()
df_oecd_jp['date'] = df_oecd_jp['date'].dt.date  # Use .dt.date to extract date from DatetimeIndex

# Convert the 'date' column in the macroeconomic DataFrame to datetime objects and then to date
df_macro_jp['date'] = pd.to_datetime(df_macro_jp['date'], format = '%Y').dt.date

### 4. Set Index ###
# Set 'country' and 'date' as the index for the macroeconomic DataFrame
df_macro_jp = df_macro_jp.set_index(['country', 'date'])

# Set 'country' and 'date' as the index for the OECD DataFrame
df_oecd_jp = df_oecd_jp.set_index(['country', 'date'])

### 5. Merge DataFrames ###
# Merge the two DataFrames based on the common index ('country', 'date') using an inner join
df_merge = pd.merge(
    df_macro_jp,
    df_oecd_jp,
    right_index = True,
    left_index = True,
    how = 'inner'
)

### 6. Export Data ###
# Ensure the 'data/intermediate/' directory exists
os.makedirs("data/intermediate/", exist_ok=True)
# Export the merged DataFrame to a CSV file in the 'data/intermediate/' directory
df_merge.to_csv("data/intermediate/merged_data_jp.csv")

# Ensure the 'data/raw/' directory exists
os.makedirs("data/raw/", exist_ok=True)
# Export the raw OECD DataFrame to a CSV file in the 'data/raw/' directory
df_oecd.to_csv("data/raw/oecd_jp.csv")