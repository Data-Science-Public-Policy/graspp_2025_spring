import pandas as pd
from global_macro_data import gmd
import os


class MacroDataPipeline:

    def __init__(self, indicators):
        self.raw_file_path = '../../../data/raw/raw_macro_data.csv'
        self.clean_file_path = '../../../data/clean/clean_macro_data.csv'
        self.df = None
        self.df_final = None  
        self.indicators = indicators

    def get_macro_data(self):        
        data_exists = os.path.exists(self.raw_file_path)
        if data_exists:
            print("Macro data file already exists")
            self.df = pd.read_csv(self.raw_file_path)
        else:
            self.df = gmd(variables = self.indicators)
            self.df.to_csv(self.raw_file_path)
        return self.df

    def rename_clean(self):
        self.df_final = self.df.rename({"ISO3":'country'}, axis=1)
        self.df_final = self.df_final.dropna(subset=self.indicators)
        data_exists = os.path.exists(self.clean_file_path)
        if data_exists:
            print("Macro data file already exists")
        else:
            self.df.to_csv(self.clean_file_path)
        return self.df_final



