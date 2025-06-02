import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from linearmodels.panel import PanelOLS
import requests
import time
from fredapi import Fred


class TradeDebtAnalyzer:
    @staticmethod
    def download_data():
        api_key_un = "53408856aa4441c8af4cf29b62aab37a"

        def get_uncomtrade_data(subscription_key: str, params: dict) -> pd.DataFrame:
            base_url = f"https://comtradeapi.un.org/data/v1/get/{params['typeCode']}/{params['freqCode']}/{params['clCode']}"
            query_params = {"subscription-key": subscription_key, **params}
            try:
                r = requests.get(base_url, params=query_params, timeout=60)
                r.raise_for_status()
                data = r.json()
                return pd.DataFrame(data["data"]) if data.get("data") else pd.DataFrame()
            except (requests.RequestException, ValueError) as err:
                print(f"Request failed: {err}")
                return pd.DataFrame()

        country_list = [36, 40, 56, 124, 208, 233, 251, 300, 348, 352,
                        372, 392, 440, 554, 703, 724, 752, 826, 842]
        dfs = []
        for country in country_list:
            for year in range(2010, 2024):
                query_cty = {
                    "typeCode": "C", "freqCode": "A", "clCode": "HS",
                    "period": f"{year}", "reporterCode": f"{country}",
                    "partnerCode": "156", "partner2Code": "0",
                    "flowCode": "M", "maxrecords": "1000", "cmdCode": "TOTAL"
                }
                time.sleep(2)
                df_cty = get_uncomtrade_data(api_key_un, query_cty)
                time.sleep(2)
                if not df_cty.empty:
                    print(df_cty.shape, country, year)
                    dfs.append(df_cty)

        df = pd.concat(dfs, ignore_index=True)
        df_all = df[df['motCode'] == 0]
        df_all_sum = df_all.groupby(['period','reporterCode'])['primaryValue'].sum().reset_index()
        df_trade = df_all_sum[df_all_sum['reporterCode'] != 528]

        fred = Fred(api_key='a8be37f8d6242d8ee6601727cf359c50')

        debt_series = {
            '36': 'DEBTTLAUA188A', '40': 'DEBTTLATA188A', '56': 'DEBTTLBEA188A',
            '124': 'DEBTTLCAA188A', '208': 'DEBTTLDEA188A', '233': 'DEBTTLEEA188A',
            '251': 'DEBTTLFRA188A', '300': 'DEBTTLGRA188A', '348': 'DEBTTLHUA188A',
            '352': 'DEBTTLISA188A', '372': 'DEBTTLIEA188A', '392': 'DEBTTLJPA188A',
            '440': 'DEBTTLLTA188A', '554': 'DEBTTLNZA188A', '703': 'DEBTTLSKA188A',
            '724': 'DEBTTLESA188A', '752': 'DEBTTLSEA188A', '826': 'DEBTTLGBA188A', '842': 'DEBTTLUSA188A'
        }

        gdp_pc_series = {
            '36': 'NYGDPPCAPKDAUS', '40': 'NYGDPPCAPKDAUT', '56': 'NYGDPPCAPKDBEL',
            '124': 'NYGDPPCAPKDCAN', '208': 'NYGDPPCAPKDDNK', '233': 'NYGDPPCAPKDEST',
            '251': 'NYGDPPCAPKDFRA', '300': 'NYGDPPCAPKDGRC', '348': 'NYGDPPCAPKDHUN',
            '352': 'NYGDPPCAPKDISL', '372': 'NYGDPPCAPKDIRL', '392': 'NYGDPPCAPKDJPN',
            '440': 'NYGDPPCAPKDLTU', '554': 'NYGDPPCAPKDNZL', '703': 'NYGDPPCAPKDSVK',
            '724': 'NYGDPPCAPKDESP', '752': 'NYGDPPCAPKDSWE', '826': 'NYGDPPCAPKDGBR', '842': 'NYGDPPCAPKDUSA'
        }

        def get_series_data(series_dict, value_column):
            all_data = []
            for country_code, series_id in series_dict.items():
                data = fred.get_series(series_id).loc['2010':'2023']
                df = data.resample('A').mean().reset_index()
                df.columns = ['year', value_column]
                df['year'] = df['year'].dt.year
                df['country'] = int(country_code)
                all_data.append(df)
            return pd.concat(all_data, ignore_index=True)

        debt_df = get_series_data(debt_series, 'debt_ratio')
        gdp_df = get_series_data(gdp_pc_series, 'gdp_per_cap')
        merged_df = pd.merge(debt_df, gdp_df, on=['year', 'country'])

        df_trade['period'] = df_trade['period'].astype(int)
        merged_df['country'] = merged_df['country'].astype(int)
        df_final = pd.merge(df_trade, merged_df, left_on=['period','reporterCode'], right_on=['year','country'])

        return df_final[['period','reporterCode','primaryValue','debt_ratio','gdp_per_cap']]

    def __init__(self, csv_path=None, download=False):
        if csv_path:
            self.df = pd.read_csv(csv_path)
        elif download:
            self.df = TradeDebtAnalyzer.download_data()
        else:
            raise ValueError("Provide either csv_path or set download=True.")

        self.code_to_country = {
            36: 'Australia', 40: 'Austria', 56: 'Belgium', 124: 'Canada', 208: 'Denmark',
            233: 'Estonia', 251: 'France', 300: 'Greece', 348: 'Hungary', 352: 'Iceland',
            372: 'Ireland', 392: 'Japan', 440: 'Lithuania', 554: 'New Zealand',
            703: 'Slovak Republic', 724: 'Spain', 752: 'Sweden', 826: 'United Kingdom', 842: 'United States'
        }
        self.df['country'] = self.df['reporterCode'].map(self.code_to_country)

        self.df = self.df.rename(columns={
            'primaryValue': 'Import from China',
            'gdp_per_cap': 'GDP per Capita',
            'debt_ratio': 'Debt Ratio (% of GDP)',
            'period': 'Year'
        })

        self.df = self.df[self.df['Year'].between(2010, 2023)]

        # Sort before lagging
        self.df = self.df.sort_values(['country', 'Year'])

        # Lag GDP and Debt by one year (within each country)
        self.df['GDP per Capita (Lag1)'] = self.df.groupby('country')['GDP per Capita'].shift(1)
        self.df['Debt Ratio (% of GDP) (Lag1)'] = self.df.groupby('country')['Debt Ratio (% of GDP)'].shift(1)
        self.df['Import from China (Lag1)'] = self.df.groupby('country')['Import from China'].shift(1)



    def plot(self):
            df = self.df.copy()

            df_long = df.melt(
                id_vars=['Year', 'country'],
                value_vars=['Import from China', 'GDP per Capita', 'Debt Ratio (% of GDP)'],
                var_name='Indicator',
                value_name='Value'
            )

            countries = df['country'].unique()
            n_cols = 4
            n_rows = -(-len(countries) // n_cols)

            fig = make_subplots(
                rows=n_rows,
                cols=n_cols,
                subplot_titles=countries,
                shared_xaxes=False,
                shared_yaxes=False,
                vertical_spacing=0.08,
                specs=[[{"secondary_y": True}]*n_cols for _ in range(n_rows)]
            )

            for i, country in enumerate(countries):
                df_c = df_long[df_long['country'] == country].sort_values('Year')
                row = i // n_cols + 1
                col = i % n_cols + 1

                for indicator in ['Import from China', 'Debt Ratio (% of GDP)']:
                    df_i = df_c[df_c['Indicator'] == indicator]
                    use_secondary_y = indicator == 'Debt Ratio (% of GDP)'
                    fig.add_trace(
                        go.Scatter(
                            x=df_i['Year'].astype(str),
                            y=df_i['Value'],
                            name=indicator if i == 0 else None,
                            mode='lines+markers',
                            line=dict(dash='dot' if 'Debt' in indicator else 'solid'),
                            hovertemplate=f'{country}<br>%{{x}}<br>{indicator}: %{{y:,.2f}}<extra></extra>'
                        ),
                        row=row,
                        col=col,
                        secondary_y=use_secondary_y
                    )

            fig.update_layout(
                height=300 * n_rows,
                title_text="Import from China, GDP per Capita, and Debt Ratio (2010–2023)<br><sup>Debt Ratio uses a separate y-axis</sup>",
                showlegend=False
            )

            for axis in fig.layout:
                if axis.startswith("xaxis"):
                    fig.layout[axis].type = 'category'

            fig.show()


    def regress(self):
        df_reg = self.df.dropna(subset=['Import from China', 'GDP per Capita', 'Debt Ratio (% of GDP)',\
                                        'GDP per Capita (Lag1)', 'Debt Ratio (% of GDP) (Lag1)', 'Import from China (Lag1)'])[
            ['country', 'Year', 'Import from China', 'GDP per Capita', 'Debt Ratio (% of GDP)','GDP per Capita (Lag1)', 'Debt Ratio (% of GDP) (Lag1)', 'Import from China (Lag1)']
        ].copy()
        df_reg = df_reg.set_index(['country', 'Year'])
        model = PanelOLS.from_formula(
            '`Debt Ratio (% of GDP)` ~ `GDP per Capita` + `Import from China (Lag1)` + EntityEffects + TimeEffects',
            data=df_reg
        )
        return model.fit(cov_type='clustered', cluster_entity=True)
