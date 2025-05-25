# run_analysis.py

from src.data.download_worldbank import DownloadWorldBank
from src.features.generate_features import GenerateFeatures
from src.viz.plot_basic import PlotBasic  # Import the visualization class
import pandas as pd

class RunPipeline:
    def __init__(self):
        self.indicators = ['BX.KLT.DINV.WD.GD.ZS', 'MS.MIL.XPND.GD.ZS', 'NY.GDP.MKTP.CD', 'NE.EXP.GNFS.ZS', 'NE.IMP.GNFS.ZS']
        self.countries = ['US', 'CA', 'MX', 'JP']
        self.date_start = '2010'
        self.date_end = '2023'
        self.rolling_window = 3
        self.features = ["changepct", "changeraw", "rollingmean", "log", "zscore", "lag1", "lag2"]
        self.time_period = 'YE'
        self.raw_data = None
        self.feature_data = None
        self.viz = PlotBasic() # Instantiate the visualization class

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

    def visualize(self, df):
        """Visualizes the provided DataFrame."""
        print('\nStep 3: Visualization')
        self.viz.plot_timeseries(
            df=df,
            y_data='NE.EXP.GNFS.ZS',
            y_feat='chpct1YE',
            x_data='NY.GDP.MKTP.CD',
            x_feat='chpct1YE',
            x_label='GDP Growth',
            y_label='Export Growth'
        )

        self.viz.plot_histogram(
            df=df,
            data_col='NY.GDP.MKTP.CD',
            feature='chpct1YE',
            label='GDP Growth',
            title='Histogram of GDP Growth',
        )

        self.viz.plot_scatter(
            df=df,
            y_data='NE.EXP.GNFS.ZS',
            y_feat='chpct1YE',
            x_data='NY.GDP.MKTP.CD',
            x_feat='chpct1YE',
            x_label='GDP Growth',
            y_label='Export Growth'
        )

    def run(self):
        """Runs the download, transform, and visualize steps sequentially."""
        self.download(save_data=False)
        if self.raw_data is not None:
            self.transform(input_df=self.raw_data)
            if self.feature_data is not None:
                print(self.feature_data.columns)
                self.visualize(self.feature_data)
            else:
                print("Feature generation failed, skipping visualization.")
        else:
            print("Download step failed, skipping transform and visualization.")

if __name__ == "__main__":
    analysis_runner = RunPipeline()
    analysis_runner.run()

    # You can also run the steps individually:
    # analysis_runner_separate = RunAnalysis()
    # raw_df = analysis_runner_separate.download()
    # if raw_df is not None:
    #     feature_df = analysis_runner_separate.transform(input_df=raw_df)
    #     analysis_runner_separate.visualize()