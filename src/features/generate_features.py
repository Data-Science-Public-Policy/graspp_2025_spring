import pandas as pd

class GenerateFeatures:
    """
    Adds time-series features to a DataFrame, grouped by 'country'.

    This class provides methods to handle feature engineering for time-series data
    across different countries.

    Attributes:
        rolling_window (int): Rolling rolling_window size for moving averages and other features.
        features (list): A list of features to include
            ("changepct", "changeraw", "rollingmean", "log", "zscore", "lag1", "lag2").
        time_period (str): Time period indicator ('D' for day, 'M' for month, etc.)

    Methods:
        transform(self, df: pd.DataFrame) -> pd.DataFrame:
    """
    def __init__(self, rolling_window=3, features=None, time_period='D'):
        """
        Initializes the FeaturesEntity.

        Args:
            rolling_window (int, optional): Rolling rolling_window size. Defaults to 3.
            features (list, optional): List of features to include.
                Defaults to ["changepct", "changeraw", "rollingmean", "zscore", "lag1", "lag2"].
            time_period (str, optional): Time period indicator ('D' for day, 'M' for month, etc.).
                Defaults to 'D'.
        """
        self.rolling_window = rolling_window
        if features is None:
            self.features = ["changepct", "changeraw", "rollingmean", "zscore", "lag1", "lag2"]
        else:
            self.features = features
        self.time_period = time_period

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Adds time-series features to a DataFrame grouped by 'country'.
        Handles both index-based and column-based 'country'.

        Args:
            df (pd.DataFrame): Input DataFrame with country/date in index or columns.

        Returns:
            pd.DataFrame: DataFrame with added features.

        Raises:
            ValueError: If the DataFrame does not have 'country' as a column or index level.
        """
        df_out = df.copy()

        # Determine group key for 'country'
        if 'country' in df_out.columns:
            group_key = df_out['country']
            group_obj = df_out.groupby('country')
        elif 'country' in df_out.index.names:
            group_key = df_out.index.get_level_values('country')
            group_obj = df_out.groupby(level='country')
        else:
            raise ValueError("DataFrame must have 'country' as a column or index level.")

        # Identify numeric columns
        num_cols = df_out.select_dtypes(include='number').columns.tolist()

        # 1. Raw first differences
        if "changeraw" in self.features:
            df_diff = group_obj[num_cols].diff().add_suffix(f'_chraw1{self.time_period}')
            df_out = pd.concat([df_out, df_diff], axis=1)

        # 2. Percentage first differences
        if "changepct" in self.features:
            df_pct_change = group_obj[num_cols].pct_change().add_suffix(f'_chpct1{self.time_period}')
            df_out = pd.concat([df_out, df_pct_change], axis=1)

        # 3. Moving average
        if "rollingmean" in self.features:
            df_ma = group_obj[num_cols].transform(lambda x: x.rolling(window=self.rolling_window, min_periods=1).mean())
            df_ma.columns = [f"{col}_ma{self.rolling_window}{self.time_period}" for col in df_ma.columns]
            df_out = pd.concat([df_out, df_ma], axis=1)

            # 4. Change in moving average
            df_ma_diff = df_ma.groupby(group_key).diff()
            df_ma_diff.columns = [f"{col}_chg{self.time_period}" for col in df_ma_diff.columns]
            df_out = pd.concat([df_out, df_ma_diff], axis=1)

        # 5. Lag features (1 and 2 steps)
        if "lag1" in self.features or "lag2" in self.features:
            for lag in [1, 2]:
                if f"lag{lag}" in self.features:
                    df_lag = group_obj[num_cols].shift(lag)
                    df_lag.columns = [f"{col}_lag{lag}{self.time_period}" for col in df_lag.columns]
                    df_out = pd.concat([df_out, df_lag], axis=1)

        # 6. Z-score within each country
        if "zscore" in self.features:
            df_zscore = group_obj[num_cols].transform(lambda x: (x - x.mean()) / x.std(ddof=0))
            df_zscore.columns = [f"{col}_zscore{self.time_period}" for col in df_zscore.columns]
            df_out = pd.concat([df_out, df_zscore], axis=1)

        # 7. Rolling std, min, and max
        if "rollingstd" in self.features:
            df_std = group_obj[num_cols].transform(lambda x: x.rolling(rolling_window=self.rolling_window, min_periods=1).std())
            df_std.columns = [f"{col}_std{self.rolling_window}{self.time_period}" for col in df_std.columns]
            df_out = pd.concat([df_out, df_std], axis=1)

        if "rollingmin" in self.features:
            df_min = group_obj[num_cols].transform(lambda x: x.rolling(rolling_window=self.rolling_window, min_periods=1).min())
            df_min.columns = [f"{col}_min{self.rolling_window}{self.time_period}" for col in df_min.columns]
            df_out = pd.concat([df_out, df_min], axis=1)

        if "rollingmax" in self.features:
            df_max = group_obj[num_cols].transform(lambda x: x.rolling(rolling_window=self.rolling_window, min_periods=1).max())
            df_max.columns = [f"{col}_max{self.rolling_window}{self.time_period}" for col in df_max.columns]
            df_out = pd.concat([df_out, df_max], axis=1)

        return df_out