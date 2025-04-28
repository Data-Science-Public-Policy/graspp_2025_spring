import pandas as pd
 import matplotlib.pyplot as plt

 def import_data(file_path):
     data = pd.read_csv(file_path)
     return data

 gdp_data = import_data('GDP.csv')   
 pop_data = import_data('POP.csv')   

 print("GDP数据列名：")
 print(gdp_data.columns)

 print("\n人口数据列名：")
 print(pop_data.columns)

 gdp_data = gdp_data[gdp_data['Gross domestic product 2022'].apply(pd.to_numeric, errors='coerce').notna()]
 pop_data = pop_data[pop_data['Population 2022'].apply(pd.to_numeric, errors='coerce').notna()]

 gdp_selected = gdp_data[['Unnamed: 0', 'Gross domestic product 2022']]
 pop_selected = pop_data[['Unnamed: 0', 'Population 2022']]

 gdp_selected = gdp_selected.rename(columns={'Unnamed: 0': 'Country Name', 'Gross domestic product 2022': 'GDP_2022'})
 pop_selected = pop_selected.rename(columns={'Unnamed: 0': 'Country Name', 'Population 2022': 'Population_2022'})

 merged_data = pd.merge(gdp_selected, pop_selected, on='Country Name')

 print("\n合并后的数据预览：")
 print(merged_data.head())

 print("\n描述性统计：")
 print(merged_data.describe())

 top10_gdp = merged_data.sort_values(by='GDP_2022', ascending=False).head(10)

 plt.figure(figsize=(10,6))
 plt.bar(top10_gdp['Country Name'], top10_gdp['GDP_2022'])
 plt.xticks(rotation=45, ha='right', fontsize=10)
 plt.title('Top 10 GDP Countries in 2022')
 plt.xlabel('Country')
 plt.ylabel('GDP (Current US$)')
 plt.tight_layout()
 plt.show()
