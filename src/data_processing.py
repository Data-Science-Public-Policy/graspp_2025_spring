import pandas as pd

# List of selected countries (ISO3 codes)
SELECTED_COUNTRIES = [
    'AND', 'ARG', 'AUS', 'ARM', 'BGD', 'BOL', 'BRA', 'CAN', 'CHL', 'CHN', 'COL', 'CYP', 'CZE', 'ECU', 'EGY', 'ETH',
    'DEU', 'GRC', 'GBR', 'GTM', 'HKG', 'IRL', 'IDN', 'IND', 'IRN', 'IRQ', 'JOR', 'JPN', 'KAZ', 'KEN', 'KGZ', 'LBN',
    'LBY', 'MDV', 'MEX', 'MYS', 'MNG', 'MAR', 'MMR', 'NLD', 'NZL', 'NIC', 'NGA', 'PAK', 'PER', 'PHL', 'PRI', 'ROU',
    'RUS', 'SGP', 'SRB', 'SVK', 'KOR', 'TJK', 'THA', 'TUR', 'TUN', 'UKR', 'USA', 'URY', 'UZB', 'VEN', 'VNM', 'ZWE'
]

def GDP_percapita(raw_path, output_path, countries=SELECTED_COUNTRIES):
    df = pd.read_csv(raw_path, skiprows=4)
    df = df[df['Country Code'].isin(countries)]

    years = [str(y) for y in range(2000, 2022)]
    df = df[['Country Name', 'Country Code'] + years]

    df_long = df.melt(
        id_vars=['Country Name', 'Country Code'],
        var_name='Year',
        value_name='GDP_percapita'
    )

    df_long = df_long.rename(columns={
        'Country Name': 'Country',
        'Country Code': 'ISO3'
    })

    df_long['Year'] = df_long['Year'].astype(int)
    df_long = df_long.sort_values(by=['Country', 'Year']).reset_index(drop=True)

    df_long.to_csv(output_path, index=False)
    return df_long

def tax_revenue(raw_path, output_path, countries=SELECTED_COUNTRIES):
    df = pd.read_csv(raw_path, skiprows=4)
    df = df[df['Country Code'].isin(countries)]

    years = [str(y) for y in range(2000, 2022)]
    df = df[['Country Name', 'Country Code'] + years]

    df_long = df.melt(
        id_vars=['Country Name', 'Country Code'],
        var_name='Year',
        value_name='TaxRevenue_percent_GDP'
    )

    df_long = df_long.rename(columns={
        'Country Name': 'Country',
        'Country Code': 'ISO3'
    })

    df_long['Year'] = df_long['Year'].astype(int)
    df_long = df_long.sort_values(by=['Country', 'Year']).reset_index(drop=True)

    df_long.to_csv(output_path, index=False)
    return df_long

def merge_gdp_tax(gdp_df, tax_df, output_path=None):
    merged_df = pd.merge(gdp_df, tax_df, on=['ISO3', 'Year'], how='inner', suffixes=('_gdp', '_tax'))
    if output_path:
        merged_df.to_csv(output_path, index=False)
    return merged_df

def describe_stats(df):
    return df[['GDP_percapita', 'TaxRevenue_percent_GDP']].describe()

import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm

def scatter_with_regression(df, x_col, y_col, title=''):
    sns.set(style="whitegrid")
    plt.figure(figsize=(8,6))
    sns.regplot(x=x_col, y=y_col, data=df, line_kws={"color": "red"})
    plt.title(title)
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.tight_layout()
    plt.show()

def run_ols(df, x_col, y_col):
    X = sm.add_constant(df[x_col])
    y = df[y_col]
    model = sm.OLS(y, X).fit()
    return model.summary()
