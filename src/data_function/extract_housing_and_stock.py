import pandas as pd

def extract_housing_and_stock(file_path: str) -> pd.DataFrame:
    """
    Extract fixed assets and stock assets from the Japanese SNA Excel file.

    Parameters:
    file_path (str): Path to the downloaded Excel file.

    Returns:
    pd.DataFrame: DataFrame containing year, fixed_asset, and stock_asset.
    """
    # Load Excel
    sheet_name = '期末貸借対照表'
    df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)

    # Set years
    years = list(range(1994, 2024))

    # Extract data
    fixed_asset_values = df.iloc[10, 1:1+len(years)].values
    stock_asset_values = df.iloc[22, 1:1+len(years)].values

    # Create DataFrame
    data = pd.DataFrame({
        'year': years,
        'fixed_asset': fixed_asset_values,
        'stock_asset': stock_asset_values
    })

    return data
