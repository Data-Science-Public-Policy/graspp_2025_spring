import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# extract the energy data from different countries in 2022
energy_path = r"D:\Users\37620\Desktop\graspp\merge（XIONG Zhenyu）\share-elec-by-source.csv"
df_energy = pd.read_csv(energy_path)
countries = ["USA", "CAN", "BRA", "ARG", "GBR", "DEU", "AUS", "NZL", "JPN", "CHN", "NGA", "ZAF"]
df_2022_energy = df_energy[df_energy["Year"] == 2022]
df_filtered = df_2022_energy[df_2022_energy["Code"].isin(countries)]

# extract
energy_columns = [col for col in df_filtered.columns if col.endswith('_share_of_electricity__pct')]
df_melted = df_filtered.melt(id_vars=["Code"], value_vars=energy_columns,
                             var_name="Energy", value_name="Share")
df_melted["Energy"] = df_melted["Energy"].str.replace("_share_of_electricity__pct", "")
df_melted["Energy"] = df_melted["Energy"].str.replace("_", " ").str.title()

# add the Per capita GDP data
gdp_path = r"D:\Users\37620\Desktop\graspp\merge（XIONG Zhenyu）\API_NY.GDP.PCAP.CD_DS2_en_csv_v2_85121.csv"
df_gdp = pd.read_csv(gdp_path, skiprows=4)
df_gdp_2022 = df_gdp[df_gdp["Country Code"].isin(countries)][["Country Code", "2022"]].dropna()
df_gdp_2022 = df_gdp_2022.rename(columns={"2022": "GDP_per_capita_2022"})

# combine the two data sets
df_plot = df_melted.merge(df_gdp_2022, left_on="Code", right_on="Country Code")

# fixed order of countries (in ascending order of GDP)
gdp_order = df_gdp_2022.sort_values(by="GDP_per_capita_2022")["Country Code"].tolist()
df_plot["Code"] = pd.Categorical(df_plot["Code"], categories=gdp_order, ordered=True)
df_plot = df_plot.sort_values("Code")

# generate charts
fig, ax1 = plt.subplots(figsize=(14, 7))

# left axis: energy structure bar chart
sns.barplot(data=df_plot, x="Code", y="Share", hue="Energy", ax=ax1)
ax1.set_ylabel("Energy Share (%)")
ax1.set_xlabel("Country")
ax1.set_ylim(0, 100)

# right axis: GDP line chart
ax2 = ax1.twinx()
gdp_avg = df_plot.groupby("Code", observed=True)["GDP_per_capita_2022"].mean()
ax2.plot(gdp_avg.index, gdp_avg.values, color="black", marker='o', linestyle='--', label="GDP per Capita")
ax2.set_ylabel("GDP per Capita (USD)")

# add annotations for GDP values
for i, (code, gdp) in enumerate(zip(gdp_avg.index, gdp_avg.values)):
    ax2.text(i, gdp + gdp * 0.05, f"${int(gdp):,}", ha='center', va='bottom', fontsize=9, color='black')

# layout
h1, l1 = ax1.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
ax1.legend(h1 + h2, l1 + l2, loc="upper left", bbox_to_anchor=(1.15, 1))

# save
plt.title("Energy Structure and GDP per Capita in 2022")
plt.tight_layout()
plt.savefig(r"D:\Users\37620\Desktop\graspp\merge（XIONG Zhenyu）\combined_overlay_plot_with_gdp_labels.png", dpi=300)
plt.show()
