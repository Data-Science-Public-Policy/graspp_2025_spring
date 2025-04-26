# Renaming the CO2 data
def rename_co2_columns(df):
    """
    Renames columns of CO2 dataset to: country, ISO3, year, co2_per_capita
    """
    return df.rename(columns={
        "Entity": "country",
        "Code": "ISO3",
        "Year": "year",
        "emissions_total_per_capita": "co2_per_capita"
    })

# Cleaning the GDP data
def clean_gdp_data(df):
    """
    Renames and selects relevant columns from World Bank GDP per capita data.
    Output: country, ISO3, year, gdp_per_capita
    """
    df_clean = df.rename(columns={
        "country": "country",
        "countryiso3code": "ISO3",
        "date": "year",
        "value": "gdp_per_capita"
    })

    # Select only the relevant columns
    df_clean = df_clean[["country", "ISO3", "year", "gdp_per_capita"]]

    # Convert year to int
    df_clean["year"] = df_clean["year"].astype(int)

    # Sort by country and year ascending
    df_clean = df_clean.sort_values(["ISO3", "year"]).reset_index(drop=True)

    return df_clean
