import pandas as pd
import matplotlib.pyplot as plt
import os

class CbiDataPipeline:

    def __init__(self):
        self.url = 'https://cbidata.org/dataset/CBIData_Romelli_2025.dta'
        self.raw_file_path = '../../../data/raw/raw_CBIData_Romelli_2025.csv'
        self.clean_file_path = '../../../data/clean/clean_CBIData_Romelli_2025.csv'
        self.df = None
        self.df_final = None  

    def get_cbi_data(self):        
        data_exists = os.path.exists(self.raw_file_path)
        if data_exists:
            print("CBI data file already exists")
            self.df = pd.read_csv(self.raw_file_path)
        else:
            self.df = pd.read_stata(self.url)
            self.df.to_csv(self.raw_file_path)
        return self.df

    def rename_clean(self):
        self.df_final = self.df.rename({"country":'country name',"iso_a3":'country'}, axis=1)
        self.df_final = self.df_final.dropna(subset=['cbie_index'])
        data_exists = os.path.exists(self.clean_file_path)
        if data_exists:
            print("CBI clean data file already exists")
        else:
            self.df.to_csv(self.clean_file_path)
        return self.df_final



