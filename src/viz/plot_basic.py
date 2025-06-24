import os
import statsmodels.api as sm
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class PlotBasic:
    def __init__(self, output_dir='reports/viz/'):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def _save_plot(self, filename):
        filepath = os.path.join(self.output_dir, f'{filename}.png')
        plt.savefig(filepath)
        plt.close()
        print(f"Saved plot to: {filepath}")

    def plot_scatter(self, df, y_data, y_feat, x_data, x_feat, x_label, y_label):
        y_col = f"{y_data}_{y_feat}" if y_feat else y_data
        x_col = f"{x_data}_{x_feat}" if x_feat else x_data
        data = df[[x_col, y_col, 'country']].dropna()
        y = data[y_col]
        X = data[x_col]
        X = sm.add_constant(X)
        model = sm.OLS(y, X)
        results = model.fit()
        print(results.summary())
        plt.figure(figsize=(8, 6))
        sns.scatterplot(data, x=x_col, y=y_col, hue='country')
        sns.lineplot(x=data[x_col], y=results.fittedvalues, color='red',
                     label=f'Regression Line (R-squared: {results.rsquared:.2f})')
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(f'{y_label} vs {x_label}')
        plt.grid(True)
        plt.legend()
        self._save_plot('scatter')

    def plot_histogram(self, df, data_col, feature=None, label='Data', title='Histogram'):
        col_name = f"{data_col}_{feature}" if feature else data_col
        bins, color, edgecolor = 10, 'skyblue', 'black'
        plt.figure(figsize=(8, 6))
        sns.histplot(df, x=col_name, bins=bins, color=color, hue='country', edgecolor=edgecolor)
        plt.xlabel(label)
        plt.ylabel('Frequency')
        plt.title(title)
        plt.grid(axis='y', alpha=0.75)
        plt.legend()
        self._save_plot('histogram')

    def plot_timeseries(self, df, y_data, y_feat, x_data, x_feat, x_label, y_label):
        y_col = f"{y_data}_{y_feat}" if y_feat else y_data
        x_col = f"{x_data}_{x_feat}" if x_feat else x_data

        fig, ax1 = plt.subplots(figsize=(10, 6))

        df[x_col].plot(ax=ax1, color='blue', label=x_label)
        ax1.set_xlabel('Year')
        ax1.set_ylabel(x_label, color='blue')
        ax1.tick_params(axis='y', labelcolor='blue')
        ax1.legend(loc='upper left')

        ax2 = ax1.twinx()
        df[y_col].plot(ax=ax2, color='red', label=y_label)
        ax2.set_ylabel(y_label, color='red')
        ax2.tick_params(axis='y', labelcolor='red')
        ax2.legend(loc='upper right')

        plt.title(f'{y_label} vs {x_label} Over Time')
        fig.tight_layout()
        self._save_plot('timeseries')

class DataProcessor:
    def __init__(self):
        self.viz = PlotBasic()

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
