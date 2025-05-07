import pandas as pd
import requests

# Download from World Bank, GDP per Capita Data
def download_worldbank(
    indicator='NY.GDP.PCAP.PP.KD',
    countries=None,
    date_start='2000',
    date_end='2023'
):
    # Default countries from World Survey reference
    if countries is None:
        countries = [
            'AND', 'ARG', 'AUS', 'ARM', 'BGD', 'BOL', 'BRA', 'CAN', 'CHL', 'CHN', 'COL', 'CYP', 'CZE', 'ECU', 'EGY', 'ETH',
            'DEU', 'GRC', 'GBR', 'GTM', 'HKG', 'IRL', 'IDN', 'IND', 'IRN', 'IRQ', 'JOR', 'JPN', 'KAZ', 'KEN', 'KGZ', 'LBN',
            'LBY', 'MDV', 'MEX', 'MYS', 'MNG', 'MAR', 'MMR', 'NLD', 'NZL', 'NIC', 'NGA', 'PAK', 'PER', 'PHL', 'PRI', 'ROU',
            'RUS', 'SGP', 'SRB', 'SVK', 'KOR', 'TJK', 'THA', 'TUR', 'TUN', 'UKR', 'USA', 'URY', 'UZB', 'VEN', 'VNM', 'ZWE'
        ]
    
    url_base = 'http://api.worldbank.org/v2/'
    country_codes = ';'.join(countries)
    url = url_base + f'country/{country_codes}/indicator/{indicator}?date={date_start}:{date_end}&format=xml&per_page=30000'
    response = requests.get(url)
    df = pd.read_xml(response.content)
    
    return df

#Download from Our World in Data, CO2 Emission per Capita Data
def fetch_co2_data(
    countries=None,
    start_year=2000,
    end_year=2023
):
    # Default countries
    if countries is None:
        countries = [
            'AND', 'ARG', 'AUS', 'ARM', 'BGD', 'BOL', 'BRA', 'CAN', 'CHL', 'CHN', 'COL', 'CYP', 'CZE', 'ECU', 'EGY', 'ETH',
            'DEU', 'GRC', 'GBR', 'GTM', 'HKG', 'IRL', 'IDN', 'IND', 'IRN', 'IRQ', 'JOR', 'JPN', 'KAZ', 'KEN', 'KGZ', 'LBN',
            'LBY', 'MDV', 'MEX', 'MYS', 'MNG', 'MAR', 'MMR', 'NLD', 'NZL', 'NIC', 'NGA', 'PAK', 'PER', 'PHL', 'PRI', 'ROU',
            'RUS', 'SGP', 'SRB', 'SVK', 'KOR', 'TJK', 'THA', 'TUR', 'TUN', 'UKR', 'USA', 'URY', 'UZB', 'VEN', 'VNM', 'ZWE'
        ]

    # Fetch the CO2 emissions per capita data
    df = pd.read_csv(
        "https://ourworldindata.org/grapher/co-emissions-per-capita.csv?v=1&csvType=full&useColumnShortNames=true",
        storage_options={'User-Agent': 'Our World In Data data fetch/1.0'}
    )

    # fetch the metadata
    metadata = requests.get(
        "https://ourworldindata.org/grapher/co-emissions-per-capita.metadata.json?v=1&csvType=full&useColumnShortNames=true"
    ).json()

    # Filter the dataframe
    CO2_clean = df[
        (df['Code'].isin(countries)) &
        (df['Year'] >= start_year) &
        (df['Year'] <= end_year)
    ]

    # Reset index for convenience
    CO2_clean = CO2_clean.reset_index(drop=True)

    return CO2_clean

def download_OurWorldData():
    return fetch_co2_data()
