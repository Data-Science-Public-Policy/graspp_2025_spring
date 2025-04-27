import pandas as pd
import requests
import io
import os

url_macro = 'https://github.com/KMueller-Lab/Global-Macro-Database/raw/refs/heads/main/data/final/chainlinked_rGDP.dta'

df_macro = pd.read_stata(url_macro)

url_oecd = "https://sdmx.oecd.org/public/rest/data/OECD.SDD.NAD,DSD_NAMAIN10@DF_TABLE1_INCOME,2.0/A.JPN........V..?dimensionAtObservation=AllDimensions&format=csv"

response = requests.get(url_oecd)
response.raise_for_status()  

data = io.StringIO(response.text)

df_oecd = pd.read_csv(data)

df_macro_jp = df_macro.query("ISO3 == 'JPN'")[['ISO3', 'year', 'UN_rGDP', 'WDI_rGDP']].dropna()

df_oecd_jp = df_oecd[['REF_AREA', 'TIME_PERIOD', 'OBS_VALUE', 'TRANSACTION', 'UNIT_MEASURE']].query("REF_AREA == 'JPN'")

df_macro_jp = df_macro_jp.rename({"ISO3": 'country', "year": 'date'}, axis=1)

df_oecd_jp = df_oecd_jp.rename({"REF_AREA": 'country', "TIME_PERIOD": 'date', 'OBS_VALUE': 'COM'}, axis=1).drop(["TRANSACTION", "UNIT_MEASURE"], axis=1)


print("Dataset shapes:")
print(f"Macro data: {df_macro_jp.shape}")
print(f"OECD data: {df_oecd_jp.shape}")

print("\nMacro data sample:")
print(df_macro_jp.head())
print("\nOECD data sample:")
print(df_oecd_jp.head())


df_macro_jp['date'] = df_macro_jp['date'].astype(int)

print("\nMacro data sample after type conversion:")
print(df_macro_jp.head())


df_macro_jp = df_macro_jp.set_index(['country', 'date'])
df_oecd_jp = df_oecd_jp.set_index(['country', 'date'])

print("\nData after setting indices:")
print("Macro data:")
print(df_macro_jp.head())
print("\nOECD data:")
print(df_oecd_jp.head())

df_merge = pd.merge(
    df_macro_jp,
    df_oecd_jp,
    right_index=True,
    left_index=True,
    how='inner'
)

print("\nMerge results:")
print(f"Merged data shape: {df_merge.shape}")
print(df_merge.head())

os.makedirs("data/homework1/", exist_ok=True)

df_merge.to_csv("data/homework1/merged_data_jp.csv")

os.makedirs("data/homework1/", exist_ok=True)

df_oecd.to_csv("data/homework1/oecd_jp.csv")

print("\nFiles saved successfully!")

print("\n" + "="*50)
print("DETAILED DATA PREVIEW AND SUMMARY")
print("="*50)

print("\nComplete Merged Dataset:")
df_merge_display = df_merge.reset_index()
print(df_merge_display)