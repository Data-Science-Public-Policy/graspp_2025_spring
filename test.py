import pandas as pd
# Skip the previous 4 lines
df = pd.read_csv(r"D:\Users\37620\Desktop\graspp\WBG\Access to electricity, urban (% of urban population)\API_EG.ELC.ACCS.UR.ZS_DS2_en_csv_v2_20800.csv", skiprows=4)
# Only keep 'Access to electricity, urban (% of urban population)'
df = df[df['Indicator Name'] == 'Access to electricity, urban (% of urban population)']

# Remove the rows where all the data in all years (columns) are empty
df = df.dropna(axis=0, how='all', subset=df.columns[4:])

# Retain the data of the two columns 'Country Name' and 'Country Code' and all years
df = df[['Country Name', 'Country Code'] + list(df.columns[4:])]

# Remove the columns whose column values are all NaN in all years
cleaned_df = df.dropna(axis=1, how='all')

# Output the first few lines and take a look
print(cleaned_df.head(6))

# save
cleaned_df.to_csv(r"D:\Users\37620\Desktop\graspp\Data sum\cleaned_data Access to electricity, urban (% of urban population).csv", index=False)
