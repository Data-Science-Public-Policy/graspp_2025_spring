# run_analysis.py

from src.data.download_worldbank import DownloadWorldBank
from src.features.generate_features import GenerateFeatures
# from src.visualization.visualize import Visualize  # Assuming you have this module
import pandas as pd

class RunAnalysis:
    def __init__(self):
        self.indicators = ['BX.KLT.DINV.WD.GD.ZS', 'MS.MIL.XPND.GD.ZS', 'NY.GDP.MKTP.CD', 'NE.EXP.GNFS.ZS', 'NE.IMP.GNFS.ZS']
        self.countries = ['US', 'CA', 'MX', 'JP']
        self.date_start = '2020'
        self.date_end = '2023'
        self.rolling_window = 3
        self.features = ["changepct", "changeraw", "rollingmean", "log", "zscore", "lag1", "lag2"]
        self.time_period = 'D'
        self.raw_data = None
        self.feature_data = None

    def download(self, save_data=False):
        """Downloads data from the World Bank."""
        print('Step 1: Download')
        download_wb = DownloadWorldBank(
            indicators=self.indicators,
            countries=self.countries,
            date_start=self.date_start,
            date_end=self.date_end
        )
        self.raw_data = download_wb.run(save_data=save_data)
        print(self.raw_data.head(2))
        return self.raw_data

    def transform(self, input_df=None, save_features=True):
        """Transforms the raw data by generating features."""
        if input_df is None:
            if self.raw_data is None:
                raise ValueError("Raw data is not available. Please run the download method first or provide an input DataFrame.")
            input_df = self.raw_data

        print('\nStep 2: Transform')
        transform_tool = GenerateFeatures(
            rolling_window=self.rolling_window,
            features=self.features,
            time_period=self.time_period
        )
        self.feature_data = transform_tool.transform(input_df)
        if save_features:
            output_path = "data/features/wb_feat.csv"
            self.feature_data.to_csv(output_path)
            print(f'Saved features here: {output_path}')
        return self.feature_data

    def run(self):
        """Runs the download and transform steps sequentially."""
        self.download(save_data=False)
        if self.raw_data is not None:
            self.transform(input_df=self.raw_data)
        else:
            print("Download step failed, skipping transform.")

        # Step 3. Viz (Placeholder)
        print('\nStep 3: Visualization (Implementation Placeholder)')
        # Assuming you have a Visualize class in src.visualization.visualize
        # You would instantiate it here and call its methods using self.feature_data.
        # Example (uncomment if you have the Visualize class):
        # if self.feature_data is not None:
        #     visualize_tool = Visualize(df=self.feature_data)
        #     visualize_tool.plot_some_features()
        # else:
        #     print("Feature generation failed, skipping visualization.")
        print('Visualization steps would be executed here if the module exists and data is available.')

if __name__ == "__main__":
    analysis_runner = RunAnalysis()
    analysis_runner.run()

    # You can also run the steps individually:
    # analysis_runner_separate = RunAnalysis()
    # raw_df = analysis_runner_separate.download()
    # if raw_df is not None:
    #     feature_df = analysis_runner_separate.transform(input_df=raw_df)