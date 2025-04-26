import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

class PipelineWBDescriptive:
    def __init__(self, indicator, countries, date_start=None, date_end=None):
        self.indicator = indicator
        self.countries = countries
        self.date_start = date_start
        self.date_end = date_end
        self.url_base = 'http://api.worldbank.org/v2/'
        self.df = None
        self.df_pivot = None
        self.df_final = None        

    def download(self, save_data=False):
        country_codes = ';'.join(self.countries)
        url = f'country/{country_codes}/indicator/{self.indicator}?per_page=30000'
        if self.date_start and self.date_end:
            url += f'&date={self.date_start}:{self.date_end}'
        url = self.url_base + url
        response = requests.get(url)
        self.df = pd.read_xml(response.content)
        self.df['series'] = self.indicator
        self.df['date'] = pd.to_datetime(self.df['date'], format="%Y")
        if save_data:
            print(f"data save here: data/raw_{self.indicator}.csv')")
            self.df.to_csv(f'data/raw_{self.indicator}.csv')
        return self.df

    def pivot(self):
        self.df_pivot = self.df.pivot(index=['countryiso3code', 'date'], columns=['series'], values='value').reset_index()
        return self.df_pivot

    def rename_convert(self, save_data=False):
        self.df_final = self.df_pivot.rename({'countryiso3code': 'country', 'date': 'date'}, axis=1)
        self.df_final['date'] = pd.to_datetime(self.df_final['date'], format='%Y')
        if save_data:
            print(f"data save here: cleaned_{self.indicator}.csv")
            self.df_final.to_csv(f'data/cleaned_{self.indicator}.csv')
        return self.df_final

    def plot_timeseries(self, title='Military Expenditure', filename=False):
        
        plt.figure(figsize=(12, 8))
        sns.lineplot(data=self.df_final, x='date', y=self.indicator, hue='country')
        plt.ylabel("GDP", size=20)
        plt.xlabel("Year", size=20)
        plt.title(title, size=20)
        plt.xticks(rotation=45, ha='right')
        plt.yticks(size=14)
        plt.tick_params(axis='both', labelsize=16)
        plt.legend(fontsize=18, loc='best')
        plt.grid(True, axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        if filename:
            print(f"time series saved here reports/{filename}")
            plt.savefig(f"reports/{filename}.png", dpi=120, bbox_inches='tight', transparent=False)
        plt.show()

    def plot_descriptive(self, title='Descriptive Statistics', filename=False):
        
        desc_stats = self.df_final.groupby("country")[self.indicator].describe().drop(['count'], axis = 'columns').transpose().plot(kind = 'barh')
        desc_stats.plot(kind='barh', figsize=(12, 8), title=title)
        plt.xlabel("Value", size=16)
        plt.ylabel("Country", size=16)
        plt.legend(fontsize=14, loc='best')
        plt.title(title)
        plt.tight_layout()
        if filename:
            print(f"time series saved here reports/{filename}")
            plt.savefig(f"reports/{filename}.png", dpi=120, bbox_inches='tight', transparent=False)
        plt.show()

# Example Usage
analyze = PipelineWBDescriptive(
    indicator='MS.MIL.XPND.GD.ZS',
    countries=['US', 'CA', 'MX', 'JP'],
    date_start='2020',
    date_end='2023'
)