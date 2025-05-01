import pandas as pd

def load_stata_url(url):
    """Load an dta file directly from a URL."""
    return pd.read_stata(url)


def merge_dataframes(df1, df2, on_column):
    """Merge two DataFrames based on a common column."""
    return pd.merge(df1, df2, on=on_column)


def clean_merged_data(df):
    """Splits merged data into two country-specific parts and stacks them together."""
    
    # Create Korea dataframe
    df_kor = df[['ISO3_x', 'year', 'CS1_pop_x', 'CS1_nGDP_x', 'CS1_rGDP', 'CS1_rGDP_pc']].copy()
    df_kor = df_kor.rename(columns={
        'ISO3_x': 'Country',
        'CS1_pop_x': 'Population',
        'CS1_nGDP_x': 'Nominal_GDP',
        'CS1_rGDP': 'Real_GDP',
        'CS1_rGDP_pc': 'Real_GDP_per_Capita'
    })

    # Create Taiwan dataframe
    df_twn = df[['ISO3_y', 'year', 'CS1_pop_y', 'CS1_nGDP_y', 'CS1_USDfx', 'CS1_nGDP_USD']].copy()
    df_twn = df_twn.rename(columns={
        'ISO3_y': 'Country',
        'CS1_pop_y': 'Population',
        'CS1_nGDP_y': 'Nominal_GDP',
        'CS1_USDfx': 'USD_Exchange_Rate',
        'CS1_nGDP_USD': 'Nominal_GDP_USD'
    })

    # Stack the two together
    df_cleaned = pd.concat([df_kor, df_twn], axis=0, ignore_index=True)
    
    return df_cleaned


def show_descriptive_stats(df):
    """Shows basic descriptive statistics of the cleaned DataFrame."""
    return df.describe()