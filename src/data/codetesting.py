
import pandas as pd
import requests
import io
import logging
import os
import pandas as pd



#url_oecd = "https://sdmx.oecd.org/public/rest/data/OECD.SDD.TPS,DSD_PDB@DF_PDB_ULC_Q,1.0/.Q.......?startPeriod=1990-Q4&format=csv"
# Fetch data from the URL
#df_oecd = pd.read_csv(url_oecd)
#print(df_oecd.columns)


# Load the .dta file into a pandas DataFrame
url = 'https://github.com/KMueller-Lab/Global-Macro-Database/raw/refs/heads/main/data/final/chainlinked_rGDP.dta'
df_rGDP = pd.read_stata(url)

# Check the first few rows to understand the structure
print(df_rGDP)
year_df = df_rGDP['year']
print(year_df)


#url_oecd = "https://sdmx.oecd.org/public/rest/data/OECD.SDD.TPS,DSD_PDB@DF_PDB_ULC_Q,1.0/.Q.......?startPeriod=1990-Q4&format=csv"
#response = requests.get(url_oecd)
#response.raise_for_status()  # Raise an exception for HTTP errors
# Read the text data into an in-memory text buffer
#data = io.StringIO(response.text)
# Read CSV data into a pandas DataFrame
#df_oecd = pd.read_csv(data)

#print(df_oecd.columns)



#url = "https://sdmx.oecd.org/public/rest/data/OECD.SDD.NAD,DSD_NAMAIN1@DF_QNA_BY_ACTIVITY_COE,1.1/Q..AUT..........?startPeriod=2023-Q4&dimensionAtObservation=AllDimensions&format=csv"

#response = requests.get(url)
#response.raise_for_status()

#data = io.StringIO(response.text)
#df = pd.read_csv(data)

#print(df.head(10))
#print(df['OBS_VALUE'])

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
url_oecd = "https://sdmx.oecd.org/public/rest/data/OECD.SDD.NAD,DSD_NAMAIN10@DF_TABLE1_INCOME,2.0/A.JPN........V..?dimensionAtObservation=AllDimensions&format=csv"
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
# Filter OECD data for Japan
df_oecd_jp = df_oecd[['REF_AREA', 'TIME_PERIOD', 'OBS_VALUE', 'TRANSACTION', 'UNIT_MEASURE']].query("REF_AREA == 'JPN'")

# Rename columns in the Japan macroeconomic DataFrame
df_macro_jp = df_macro_jp.rename({"ISO3": 'country', "year": 'date'}, axis=1)

# Rename columns and drop unnecessary columns in the Japan OECD DataFrame
df_oecd_jp = df_oecd_jp.rename({"REF_AREA": 'country', "TIME_PERIOD": 'date', 'OBS_VALUE': 'COM'}, axis=1).drop(["TRANSACTION", "UNIT_MEASURE"], axis=1)

# Print debug information before index conversion
print("Dataset shapes:")
print(f"Macro data: {df_macro_jp.shape}")
print(f"OECD data: {df_oecd_jp.shape}")

print("\nMacro data sample:")
print(df_macro_jp.head())
print("\nOECD data sample:")
print(df_oecd_jp.head())

### 3. Ensure Index Types Match ###
# Convert date column in macro data to integer type
df_macro_jp['date'] = df_macro_jp['date'].astype(int)

print("\nMacro data sample after type conversion:")
print(df_macro_jp.head())

### 4. Set Index ###
# Set 'country' and 'date' as the index for both DataFrames
df_macro_jp = df_macro_jp.set_index(['country', 'date'])
df_oecd_jp = df_oecd_jp.set_index(['country', 'date'])

print("\nData after setting indices:")
print("Macro data:")
print(df_macro_jp.head())
print("\nOECD data:")
print(df_oecd_jp.head())

### 5. Merge DataFrames ###
# Merge the two DataFrames based on the common index ('country', 'date') using an inner join
df_merge = pd.merge(
    df_macro_jp,
    df_oecd_jp,
    right_index=True,
    left_index=True,
    how='inner'
)

# Print merging result
print("\nMerge results:")
print(f"Merged data shape: {df_merge.shape}")
print(df_merge.head())

### 6. Export Data ###
# Ensure the 'data/intermediate/' directory exists
os.makedirs("data/intermediate/", exist_ok=True)
# Export the merged DataFrame to a CSV file in the 'data/intermediate/' directory
df_merge.to_csv("data/intermediate/merged_data_jp.csv")

# Ensure the 'data/raw/' directory exists
os.makedirs("data/raw/", exist_ok=True)
# Export the raw OECD DataFrame to a CSV file in the 'data/raw/' directory
df_oecd.to_csv("data/raw/oecd_jp.csv")

print("\nFiles saved successfully!")

### 7. Data Preview and Summary ###
print("\n" + "="*50)
print("DETAILED DATA PREVIEW AND SUMMARY")
print("="*50)


# Show merged data with original indices
print("\nComplete Merged Dataset:")
df_merge_display = df_merge.reset_index()
print(df_merge_display)

