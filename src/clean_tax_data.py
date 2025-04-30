import pandas as pd

SELECTED_COUNTRIES = [
    'AND', 'ARG', 'AUS', 'ARM', 'BGD', 'BOL', 'BRA', 'CAN', 'CHL', 'CHN', 'COL', 'CYP', 'CZE', 'ECU', 'EGY', 'ETH',
    'DEU', 'GRC', 'GBR', 'GTM', 'HKG', 'IRL', 'IDN', 'IND', 'IRN', 'IRQ', 'JOR', 'JPN', 'KAZ', 'KEN', 'KGZ', 'LBN',
    'LBY', 'MDV', 'MEX', 'MYS', 'MNG', 'MAR', 'MMR', 'NLD', 'NZL', 'NIC', 'NGA', 'PAK', 'PER', 'PHL', 'PRI', 'ROU',
    'RUS', 'SGP', 'SRB', 'SVK', 'KOR', 'TJK', 'THA', 'TUR', 'TUN', 'UKR', 'USA', 'URY', 'UZB', 'VEN', 'VNM', 'ZWE'
]

def clean_tax_data(raw_path, output_path, countries=SELECTED_COUNTRIES):
    df = pd.read_csv(raw_path, skiprows=4)

    df = df[df['Country Code'].isin(countries)]

    years = [str(y) for y in range(2000, 2021)]
    df = df[['Country Name', 'Country Code'] + years]

    df_long = df.melt(
        id_vars=['Country Name', 'Country Code'],
        var_name='Year',
        value_name='Tax_Revenue'
    )

    df_long = df_long.rename(columns={
        'Country Name': 'Country',
        'Country Code': 'ISO3'
    })

    df_long['Year'] = df_long['Year'].astype(int)
    df_long = df_long.sort_values(by=['Country', 'Year']).reset_index(drop=True)

    df_long.to_csv(output_path, index=False)
    return df_long