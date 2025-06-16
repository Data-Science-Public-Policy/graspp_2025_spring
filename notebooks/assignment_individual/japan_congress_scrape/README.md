# Japanese Congress Industry Mentions Scraper

This project scrapes the [Yonalog](https://chiholog.net/yonalog/search.html) website to analyze mentions of different industries in Japanese congress proceedings. The scraper collects data about how frequently various industries are discussed in the congress records over time.

## Overview

The project uses Selenium to interact with the Yonalog search interface and extracts time series data showing the frequency of industry mentions from 1947 to 2024. The data is collected for various industries defined in the Japanese Industrial Classification system.

## Features

- Automated scraping of industry mentions from Yonalog
- Support for multiple industry keywords per search
- Time series data from 1947 to 2024
- Checkpoint system to resume interrupted scraping
- Output in CSV format with industry IDs and mention counts

## Requirements

- Python 3.10 or higher
- Chrome browser installed
- Required Python packages (see requirements.txt)

## Installation

1. Clone this repository
2. Install the required packages:

```bash
pip install -r requirements.txt
```

## Usage

The main script is provided as a Jupyter notebook (`scrape_congress.ipynb`). To use it:

1. Open the notebook in Jupyter
2. Run the cells sequentially
3. The script will:
   - Process industry names from the classification system
   - Scrape mention counts for each industry
   - Save results to `gikai_mention.csv`

The output CSV file contains:

- Years as index (1947-2024)
- Industry names as columns
- Mention counts as values
- Industry IDs in the first row

## Data Source

The data is scraped from [Yonalog](https://chiholog.net/yonalog/search.html), a search system for Japanese congress proceedings.

## Notes

- The scraping process includes delays to avoid overloading the server
- A checkpoint system is implemented to save progress and allow resuming interrupted scraping
- Industry names are processed to handle various formats and special cases

## License

This project is for research purposes only. Please respect the terms of service of the data source website.
