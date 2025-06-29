import pandas as pd
import requests
import io
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class DataProcessor:
    def __init__(self, macro_url, oecd_url, intermediate_dir="data/intermediate/", raw_dir="data/raw/"):
        self.macro_url = macro_url
        self.oecd_url = oecd_url
        self.intermediate_dir = intermediate_dir
        self.raw_dir = raw_dir
        self.df_macro = None
        self.df_oecd = None
        self.df_macro_nz = None
        self.df_oecd_nz = None
        self.df_merge = None

    def _download_macro_data(self):
        logging.info(f"Fetching macroeconomic data from: {self.macro_url}")
        self.df_macro = pd.read_stata(self.macro_url)
        logging.info(f"Macroeconomic data loaded successfully with shape: {self.df_macro.shape}")
        # logging.info("Displaying head of macroeconomic data:")
        # logging.info(self.df_macro.head(2))

    def _download_oecd_data(self):
        logging.info(f"Fetching OECD data from: {self.oecd_url}")
        response = requests.get(self.oecd_url)
        response.raise_for_status()
        data = io.StringIO(response.text)
        self.df_oecd = pd.read_csv(data)
        logging.info(f"OECD data loaded successfully with shape: {self.df_oecd.shape}")
        # logging.info("Displaying head of OECD data:")
        # logging.info(self.df_oecd.head(2))

    def download_data(self):
        self._download_macro_data()
        self._download_oecd_data()

    def _filter_macro_nz(self):
        self.df_macro_nz = self.df_macro.query("ISO3 == 'NZL'")[['ISO3', 'year', 'OECD_KEI_infl', 'BIS_infl']].dropna()
        logging.info(f"Filtered macroeconomic data for NZL with shape: {self.df_macro_nz.shape}")
        # logging.info("Displaying tail of filtered macroeconomic data for NZL:")
        # logging.info(self.df_macro_nz.tail(2))

    def _filter_oecd_nz(self, cols=['REF_AREA', 'TIME_PERIOD', 'OBS_VALUE', 'MEASURE', 'UNIT_MEASURE']):
        self.df_oecd_nz = self.df_oecd[cols].query("REF_AREA == 'NZL' & MEASURE=='ULCE' & UNIT_MEASURE == 'PA'")
        logging.info(f"Filtered OECD data for NZL with shape: {self.df_oecd_nz.shape}")
        # logging.info("Displaying head of filtered OECD data for NZL:")
        # logging.info(self.df_oecd_nz.head(2))

    def filter_data(self):
        self._filter_macro_nz()
        self._filter_oecd_nz()

    def _rename_macro_nz(self, rename_dict={"ISO3":'country', "year":'date'}):
        self.df_macro_nz = self.df_macro_nz.rename(rename_dict, axis=1)
        logging.info("Renamed columns in macroeconomic data for NZL.")
        # logging.info("Displaying head of renamed macroeconomic data for NZL:")
        # logging.info(self.df_macro_nz.head(2))

    def _rename_oecd_nz(self, rename_drop_dict={"REF_AREA":'country', "TIME_PERIOD":'date', 'OBS_VALUE':'ULCE'}, drop_cols=["MEASURE", "UNIT_MEASURE"]):
        self.df_oecd_nz = self.df_oecd_nz.rename(rename_drop_dict, axis=1).drop(drop_cols, axis=1)
        logging.info("Renamed and dropped columns in OECD data for NZL.")
        # logging.info("Displaying head of renamed OECD data for NZL:")
        # logging.info(self.df_oecd_nz.head(2))

    def rename_columns(self):
        self._rename_macro_nz()
        self._rename_oecd_nz()

    def _convert_datetime_oecd(self):
        self.df_oecd_nz['date'] = pd.PeriodIndex(self.df_oecd_nz['date'], freq='Q').to_timestamp().date
        logging.info("Converted 'date' column in OECD data for NZL to datetime.date.")
        # logging.info(f"Data type of 'date' in OECD data for NZL: {self.df_oecd_nz['date'].dtype}")

    def _convert_datetime_macro(self):
        self.df_macro_nz['date'] = pd.to_datetime(self.df_macro_nz['date'], format = '%Y').dt.date
        logging.info("Converted 'date' column in macroeconomic data for NZL to datetime.date.")
        # logging.info(f"Data type of 'date' in macroeconomic data for NZL: {self.df_macro_nz['date'].dtype}")

    def convert_datetime(self):
        self._convert_datetime_oecd()
        self._convert_datetime_macro()

    def _set_index_macro(self, index_cols=['country', 'date']):
        self.df_macro_nz = self.df_macro_nz.set_index(index_cols)
        logging.info("Set index for macroeconomic data for NZL.")
        # logging.info("Displaying head of indexed macroeconomic data for NZL:")
        # logging.info(self.df_macro_nz.head(2))

    def _set_index_oecd(self, index_cols=['country', 'date']):
        self.df_oecd_nz = self.df_oecd_nz.set_index(index_cols)
        logging.info("Set index for OECD data for NZL.")
        # logging.info("Displaying head of indexed OECD data for NZL:")
        # logging.info(self.df_oecd_nz.head(2))

    def set_index(self):
        self._set_index_macro()
        self._set_index_oecd()

    def _merge_dataframes(self, merge_params={'right_index': True, 'left_index': True, 'how': 'inner'}):
        self.df_merge = pd.merge(self.df_macro_nz, self.df_oecd_nz, **merge_params)
        logging.info(f"Merged DataFrames with shape: {self.df_merge.shape}")
        # logging.info("Displaying tail of merged DataFrame:")
        # logging.info(self.df_merge.tail(2))

    def merge_data(self):
        self._merge_dataframes()

    def _export_merged_data(self, filename="merged_data_nz.csv"):
        os.makedirs(self.intermediate_dir, exist_ok=True)
        filepath = os.path.join(self.intermediate_dir, filename)
        self.df_merge.to_csv(filepath)
        logging.info(f"Exported merged DataFrame to {filepath}")

    def _export_raw_oecd_data(self, filename="oecd.csv"):
        os.makedirs(self.raw_dir, exist_ok=True)
        filepath = os.path.join(self.raw_dir, filename)
        self.df_oecd.to_csv(filepath)
        logging.info(f"Exported raw OECD DataFrame to {filepath}")

    def export_data(self):
        self._export_merged_data()
        self._export_raw_oecd_data()

    def run_pipeline(self):
        self.download_data()
        self.filter_data()
        self.rename_columns()
        self.convert_datetime()
        self.set_index()
        self.merge_data()
        self.export_data()

macro_url = 'https://github.com/KMueller-Lab/Global-Macro-Database/raw/refs/heads/main/data/final/chainlinked_infl.dta'
oecd_url = "https://sdmx.oecd.org/public/rest/data/OECD.SDD.TPS,DSD_PDB@DF_PDB_ULC_Q,1.0/.Q.......?startPeriod=1990-Q4&format=csv"
processor = DataProcessor(macro_url, oecd_url)