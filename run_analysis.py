# run_analysis.py

from src.data.download_worldbank import DownloadWorldBank
from src.features.generate_features import GenerateFeatures
import pandas as pd

# Step 1. Downloading
print('Step 1: Download')
download_wb = DownloadWorldBank(
    indicators=['BX.KLT.DINV.WD.GD.ZS', 'MS.MIL.XPND.GD.ZS', 'NY.GDP.MKTP.CD', 'NE.EXP.GNFS.ZS', 'NE.IMP.GNFS.ZS'],
    countries=['US', 'CA', 'MX', 'JP'],
    date_start='2020',
    date_end='2023'
)
df_wb_raw = download_wb.run(save_data = False)
df_wb_raw.head(2)

# Step 2. Transforming
print('Step 2: Transform')
transform_tool = GenerateFeatures(
    rolling_window=3,
    features=["changepct", "changeraw", "rollingmean", "log", "zscore", "lag1", "lag2"],
    time_period='D'
)

df_wb_feat = transform_tool.transform(df_wb_raw)
print('Saved features here: data/features/wb_feat.csv')
df_wb_feat.to_csv("data/features/wb_feat.csv")

# Step 3. Viz
df_wb_feat