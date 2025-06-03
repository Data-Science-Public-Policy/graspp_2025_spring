# Clan Culture and Family Farms in Rural China
This project investigates how the strength of **clan culture** affects the development of **family farms** across Chinese cities.

## Research Question
How does the strength of clan culture influence the spatial distribution and number of family farms in rural China?

Hypothesis:
The intensity of clan culture (as measured by cumulative genealogical records per capita) is positively associated with the number of family farms.

## Background

**What is Clan Culture?**  
Clan culture in China refers to lineage-based social organization centered on shared ancestry, kinship norms, and patriarchal hierarchy. It is often expressed through ancestral halls, rituals, and the compilation of genealogical records.  

**Why might clan culture influence family farming?**  
In rural China, clan networks serve as important informal institutions. Strong clan culture can:
- Enhance trust and cooperation among households;
- Reduce transaction costs and encourage joint agricultural efforts;
- Facilitate land use coordination and information sharing.

These mechanisms may enable households to more easily transition to family farm models, which require a degree of autonomy, scale, and local cooperation.

## What I Did
The full workflow is documented step-by-step in [`notebooks/analysis.ipynb`](notebooks/analysis.ipynb). 

| Section |                                                                                                                                                                   |
|--------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Part 1: Data Collection** |                                                                       |
| **Part 2: Data Transformation and Merging** | 
| **Part 3: Descriptive Statistics** |                                                                                                                                                    
| **Part 4: Visualization** | 
| **Part 5: Dashboard** |


## Data Sources
- **Genealogy Data**: Extracted from the [Shanghai Genealogy Library Online Catalog](https://www.library.sh.cn/family/)
- **Family Farm Data**: China Academy for Rural Development – Qiyan China Agri-research Database (CCAD)
- **Control Variables**: China City Statistical Yearbook (2013–2023)
  - Variables include GDP per capita, population, fiscal expenditure, arable land, etc.

LiaoYan_HW2/
├── data/
│   ├── city_data_panel.xlsx           # City-level socioeconomic data
│   ├── family_farms.xlsx              # Family farm statistics
│   ├── data_raw_genealogy_En.csv      # Raw scraped genealogy records
│   ├── genealogy_panel.csv            # Aggregated genealogy panel
│   └── dataset.csv                    # Final merged dataset
│
├── figures/
│   ├── plot_clan_vs_farms_scatter.png # Scatter: clan vs family farms
│   ├── plot_clan_vs_farms_regline.png # Regression line only
│   └── plot_clan_vs_farms_with_fit.png# Combined scatter + fit
│
├── notebooks/
│   └── analysis.ipynb                 # Full analysis: stats, charts, cases
│
├── src/
│   ├── download_genealogies.py        # Scrape genealogy records
│   ├── transform_genealogies.py       # Clean and reshape to panel format
│   ├── pipeline_main_genealogies.py   # Run full pipeline
│   └── dashboard.py                   # Streamlit dashboard
│
├── tools/
│   └── chromedriver-win64/            # ChromeDriver for Selenium
│
└── README.md                          # Project documentation

