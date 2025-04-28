import pandas as pd

def extract_employment_income(file_path: str) -> pd.DataFrame:
    """
    Extract employment income time series from the downloaded Excel file.
    
    Parameters:
    - file_path (str): Path to the downloaded employment income Excel file.

    Returns:
    - pd.DataFrame: Cleaned dataframe with 'year' and 'employment_income' columns.
    """
    # Load Excel file
    df = pd.read_excel(file_path, header=None)

    # Extract the 8th row (index 7)
    data_row = df.iloc[7]

    # Set up year range
    years = list(range(1994, 2024))

    # Only keep relevant values
    income_values = data_row[1:len(years)+1].values

    # Create DataFrame
    result_df = pd.DataFrame({
        'year': years,
        'employment_income': income_values
    })

    return result_df
