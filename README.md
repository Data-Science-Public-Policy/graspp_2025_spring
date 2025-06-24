# Objectives

My objective is to create a de facto central bank independence tracker using country reports published by The Economist Intelligence Unit (EIU) using machine learning. The methodology adopts the narrative approach described in this article:

Carola Conces Binder, “Political Pressure on Central Banks,” Journal of Money, Credit and Banking 53, no. 4 (June 2021): 715–44, https://doi.org/10.1111/jmcb.12772.

## Tracking pressure on central bank

After downloading EIU country reports from proquest, they are checked for the certain keywords and categorized as follows:

Category 2 - when the central bank succumbs to pressure to modify monetary policy:
            "under pressure", "print money", "money printing", "monetize", "succumb",
            "government control", "forced to", "pressure to lower rates"

Category 1 - when the central bank resists pressure to modify monetary policy:

            "resist", "reiterated", "independent", "declined", "not considering",
            "maintained independence", "held steady"

## Tracking threats to central bank independence

Similar to checking for pressure, reports are checked for centrain keywords and classified as follows:

legal_amendment - when threats consist of modifying central bank law to decrease independence:
            "legal independence", "revise central bank law", "amend mandate",
            "revoke independence", "constitutional change", "change in mandate"

leader_change - when threats consist of replacing the central bank governor
            "replace governor", "removed from office", "new central bank head",
            "dismissal", "reshuffle", "appointed", "sacked", "fired"

## Mentions of Elections

This is to check whether pressure on central banks or threats to their independence coincides with upcoming elections


## Misc. Notes

Initially, my plan was to download central bank laws and replicate Romelli's CBI index using LLMs. I did download the files successfully but it was difficult to process them. The laws are long, which required many tokens. I also got stuck when dealing with amendments. In any case, I am uploading the python source files and the downloaded central bank laws in parquet format.

# Notebook
- notebooks/assignment_individual_HW2_LazoHilton.ipynb
    - contains the notebook for running the code and producing the outputs

# Source Codes
- src/data/reports_processory.py: contains the code for processing the raw EIU reports
- src/data/download_cb_laws.py: downloads central bank laws 
- src/data/download_cbidate.py: downloads and processes CBI index from the Romelli dataset (adapted from monetary policy group repo)
- src/data/download_macrodata.py: downloads and processes ltrate data from the global macro database (adapted from monetary policy group repo)
- src/data/country_list.py: just plain list of countries grouped alphabetically

# Sources
- EIU Reports
    - Downloaded from Proquest using the following query:

        publisher(The Economist Intelligence Unit) AND ("central bank" OR "monetary policy" OR "reserve" bank " or " national bank "") AND ("political pressure" OR "political interference" OR "government interference" OR "threat to independence" OR "independence threatened" OR "print money" OR "money printing" "monetize" OR "monetise")

- Central Bank Independence (Romelli dataset)
    - https://cbidata.org/dataset/CBIData_Romelli_2025.dta
- Global Macro Database Python Package
    - https://github.com/KMueller-Lab/Global-Macro-Database-Python
- CBI Laws (Romelli compilation)
    - https://cbidata.org/legislations

# Raw Data File Paths
- data/raw/eiu_country_reports/eiu_country_reports_{number}.txt
    - Raw EIU country reports from Proquest; contains 100 country reports per text file
- data/raw/legislations/{Country}.parquet
    - Central Bank laws for each country

# Processed Data File Paths
- data/intermediate/eiu_reports_by_country/{country}.parquet
    - Country reports that mention keywords aggregated by country


# Future plans
- Some EIU reports are in pdf format and were not processed. Explore Proquest TDM studio in downloading reports.
- Refine the filtering mechanism for the EIU reports, account for variations in the names of central banks across countries
- Employ LLMs to categorize reports more accurately
- Check samples for accuracy of LLM categorization
- Write analysis into a paper