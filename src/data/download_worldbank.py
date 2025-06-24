import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

class DownloadWorldBank:
    def __init__(self, indicators, countries, date_start=None, date_end=None):
        self.indicators = indicators
        self.countries = countries
        self.date_start = date_start
        self.date_end = date_end
        self.url_base = 'http://api.worldbank.org/v2/'
        self.dfs = {}
        self.dfs_pivot = {}
        self.dfs_final = {}

    def download(self, indicator, save_data=False):
        country_codes = ';'.join(self.countries)
        url = f'country/{country_codes}/indicator/{indicator}?per_page=30000'
        if self.date_start and self.date_end:
            url += f'&date={self.date_start}:{self.date_end}'
        url = self.url_base + url
        response = requests.get(url)
        df = pd.read_xml(response.content)
        df['series'] = indicator
        df['date'] = pd.to_datetime(df['date'], format="%Y")
        self.dfs[indicator] = df
        if save_data:
            print(f"data save here: data/raw_{indicator}.csv")
            df.to_csv(f'data/raw_{indicator}.csv')
        return df

    def pivot(self, indicator):
        self.dfs_pivot[indicator] = self.dfs[indicator].pivot(index=['countryiso3code', 'date'], columns=['series'], values='value').reset_index()
        return self.dfs_pivot[indicator]

    def rename_convert(self, indicator):
        self.dfs_final[indicator] = self.dfs_pivot[indicator].rename({'countryiso3code': 'country', 'date': 'date'}, axis=1)
        self.dfs_final[indicator]['date'] = pd.to_datetime(self.dfs_final[indicator]['date'], format='%Y')
        return self.dfs_final[indicator]

    def run(self, save_data=False):
        merged_df = None
        for i, indicator in enumerate(self.indicators):
            print(f"Processing indicator: {indicator}")
            # Download the data
            self.download(indicator)

            # Pivot the data
            self.pivot(indicator)

            # Rename and convert the data
            self.rename_convert(indicator)

            if merged_df is None:
                merged_df = self.dfs_final[indicator]
            else:
                merged_df = pd.merge(merged_df, self.dfs_final[indicator], on=['country', 'date'], how='outer')

        if save_data:
            print(f"data save here: data/clean/merged_wb.csv")
            self.dfs_final[indicator].to_csv("data/clean/merged_wb.csv")
        return merged_df
        

if __name__ == '__main__':
    # Example Usage
    analyze = DownloadWorldBank(
        indicators=['MS.MIL.XPND.GD.ZS', 'NY.GDP.MKTP.CD', 'NE.EXP.GNFS.ZS'],
        countries=['US', 'CA', 'MX', 'JP'],
        date_start='2020',
        date_end='2023'
    )

    final_data = analyze.run(save_data=True)