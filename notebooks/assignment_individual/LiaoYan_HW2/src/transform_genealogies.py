import pandas as pd
import os

def transform_genealogy_data(input_path, output_path):
    """
    Clean and aggregate genealogy data into a province-city-year panel format.

    Parameters:
        input_path (str): Path to the raw genealogy data CSV file.
        output_path (str): Path to save the cleaned panel CSV.
    """
    df = pd.read_csv(input_path)

    df = df.dropna(subset=["Province", "City", "Compiled Time"])

    df = df[df["Compiled Time"].astype(str).str.isdigit()]
    df["Compiled Time"] = df["Compiled Time"].astype(int)


    grouped = df.groupby(["Province", "City", "Compiled Time"]).size().reset_index(name="Genealogy_Count")

    grouped = grouped.rename(columns={
        "Compiled Time": "Year"
    })

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    grouped.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"✅ Genealogy panel data saved to: {output_path}")


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, ".."))
    input_path = os.path.join(project_root, "data", "data_raw_genealogy_En.csv")
    output_path = os.path.join(project_root, "data", "genealogy_panel.csv")

    transform_genealogy_data(input_path=input_path, output_path=output_path)
