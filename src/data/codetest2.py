import pandas as pd

url = "https://github.com/paigek01/GRASSP2025_AgriEcon/raw/refs/heads/Paige-Koizumi/data/raw/data/cleaned_data.csv"

df = pd.read_csv(url)

print(df.columns)