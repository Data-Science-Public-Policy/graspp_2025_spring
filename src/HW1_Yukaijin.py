# Step2 Define Functions
def load_rice_mps(file_path):
    """
    Load the 'TOTAL' sheet from the Excel file and extract the Market Price Support (MPS) data for Rice.
    """
    # Read the entire sheet
    df = pd.read_excel(file_path, sheet_name='TOTAL', header=None)

    # Find the row that contains 'Rice' (searching within the second column)
    rice_row_index = df[df[1].astype(str).str.contains('Rice', na=False, case=False)].index[0]

    # Extract data from column 'at' to 'ce' (Python index 45 to 82)
    rice_values = df.iloc[rice_row_index, 45:83].values

    # Generate a list of years from 1986 to 2023
    years = list(range(1986, 2024))

    # Create a clean DataFrame
    df_rice = pd.DataFrame({
        'Year': years,
        'MPS_Value': rice_values
    })

    return df_rice