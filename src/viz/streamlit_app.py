import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

st.title("Interactive Emissions Plot")
st.markdown("Select countries to visualize their emissions over time.")
url = "https://github.com/Graspp-25-Spring/GraSPP-25S-climatechange/raw/refs/heads/main/data/raw/EDGAR_2024_GHG_booklet_2024.xlsx"
df = pd.read_excel(url, sheet_name="GHG_totals_by_country", header=0)
df_long = df.set_index(['Country']).drop(['EDGAR Country Code'], axis=1).stack().to_frame('emissions')
df_long = df_long.reset_index().rename({"level_1":'year'}, axis='columns')

countries =  ['Indonesia', 'India', 'Ireland']
df_short = df_long.copy().query("Country in @countries")

df_long = df.set_index(['Country']).drop(['EDGAR Country Code'], axis=1).stack().to_frame('emissions')
df_long = df_long.reset_index().rename({"level_1":'year'}, axis='columns')

selected_countries = st.multiselect(
    "Select Countries",
    options=list(df_short['Country'].unique()),
    default=list(df_short['Country'].unique())[0] if list(df_short['Country'].unique()) else None
)

fig, ax = plt.subplots()
if selected_countries:
    sns.lineplot(
        df_short.query("Country in @selected_countries"),
        x='year',
        y='emissions',
        hue='Country',
        ax=ax
    )
    ax.set_xlabel("Year")
    ax.set_ylabel("Emissions")
    ax.set_title("Emissions Over Time by Country")
    st.pyplot(fig)
else:
    st.warning("Please select at least one country.")