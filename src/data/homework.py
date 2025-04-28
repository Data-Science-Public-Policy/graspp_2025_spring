import pandas as pd
import requests
import io 
import os

url_iadb = 'https://data.iadb.org/file/download/621615a3-45d5-4c91-99bf-2d4dbee14b8e'
df_iadb = pd.read_csv(url_iadb)

print (df_iadb['country_id'])

url_iadb2 = 'https://data.iadb.org/file/download/fe4f3683-647c-44f4-a17c-022f22a922a8'
df_iadb2 = pd.read_stata(url_iadb2)

print(df_iadb2['isocode'])