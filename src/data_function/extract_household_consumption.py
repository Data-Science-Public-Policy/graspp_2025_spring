import pandas as pd

def extract_household_consumption(filepath: str) -> pd.DataFrame:
    """
    Extract household consumption time series from the downloaded Excel file.

    Args:
        filepath (str): File path to the Excel file.

    Returns:
        pd.DataFrame: A DataFrame with columns 'year' and 'household_consumption'.
    """
    # Load the Excel file without headers
    df = pd.read_excel(filepath, header=None)

    # Household consumption is located at row 9 (index 8)
    consumption_row = df.iloc[8]

    # Create years from 1994 to 2023
    years = list(range(1994, 2024))

    # Get household consumption values (skip the first column A)
    values = consumption_row[1:len(years)+1].tolist()

    # Combine into a DataFrame
    result = pd.DataFrame({
        "year": years,
        "household_consumption": values
    })

    return result
