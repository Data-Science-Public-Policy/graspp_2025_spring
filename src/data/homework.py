 import pandas as pd
import requests
import io 
import os

url_iadb = 'https://data.iadb.org/file/download/621615a3-45d5-4c91-99bf-2d4dbee14b8e'
df_iadb = pd.read_csv(url_iadb)

print (df_iadb.head())