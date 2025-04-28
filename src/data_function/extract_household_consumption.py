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

    # Year information is located at row 6 (index 5)
    years = df.iloc[5, 1:].tolist()  # Columns starting from column B
    values = consumption_row[1:].tolist()

    # Combine into a DataFrame
    result = pd.DataFrame({
        "year": years,
        "household_consumption": values
    })

    return result
