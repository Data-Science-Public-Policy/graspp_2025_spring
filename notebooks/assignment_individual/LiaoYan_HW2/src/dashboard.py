import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

st.set_page_config(page_title="Family Farms Dashboard", layout="wide")

script_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(script_dir, "..", "data", "dataset.csv")

try:
    df = pd.read_csv(data_path)
except FileNotFoundError:
    st.error("Dataset not found. Please check that 'dataset.csv' exists in the data/ folder.")
    st.stop()


st.title("Family Farms Dashboard")
st.markdown("""
This dashboard visualizes the development of family farms across Chinese cities.
""")

city = st.selectbox("Select a city:", sorted(df["city_name"].unique()))
df_city = df[df["city_name"] == city].sort_values("year")

st.subheader(f"Time Series: {city}")

fig1, ax1 = plt.subplots(figsize=(10, 4))
ax1.plot(df_city["year"], df_city["total_family_farms"], label="Family Farms", marker="o")
ax1.set_xlabel("Year")
ax1.set_ylabel("Value")
ax1.legend()
ax1.grid(True)
st.pyplot(fig1)


with st.expander("View city-level raw data"):
    st.dataframe(df_city[["year", "genealogy_count", "clan_intensity_cumsum_log", "total_family_farms"]])



