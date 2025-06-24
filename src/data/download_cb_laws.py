import os
import requests
import pandas as pd
import json
from bs4 import BeautifulSoup
from io import BytesIO
import fitz
from urllib.parse import quote
import time
import random
import pytesseract 
from PIL import Image 
from pdf2image import convert_from_path
import tempfile
import unicodedata
import urllib.parse

import sys
sys.path.append("../../../")
from src.data.country_list import CountryList


class PipielineCBLaws:

    def __init__(self):
        # Site relies on AJAX which returns the table of laws in json format
        self.laws_url = "https://cbidata.org/legislations/legislations_list.json?search="
        self.df_laws = None
        self.countries = CountryList().countries

    def fetch_law_urls(self, save_urls = False):
        
        print("Accessing search results for legislations")
        response = requests.get(self.laws_url)
        response.raise_for_status()  

        print("Parsing search results")
        data = response.json()

        records = []
        for item in data:
            country_institution = item.get("Country / Institution")
            year_month = item.get("Year-Month")
            doc_type = item.get("Type")
            title = item.get("Title")
            language = item.get("Language")

            # Parse the pdf link from the HTML
            link_html = item.get("Link")
            if link_html:
                soup = BeautifulSoup(link_html, "html.parser")
                pdf_elem = soup.find("a")
                pdf_url = pdf_elem["href"] if pdf_elem else None
            else:
                pdf_url = None

            records.append({
                "Country/Institution": country_institution,
                "Year-Month": year_month,
                "Type": doc_type,
                "Title": title,
                "Language": language,
                "pdf_url": pdf_url
            })

        if save_urls:
            # Save to JSON
            save_dir = "../../../data/raw/"
            os.makedirs(save_dir, exist_ok=True)
            file_path = os.path.join(save_dir, "legislation_pdf_urls.json")

            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(records, f, indent=2, ensure_ascii=False)

            print(f"pdf urls have been saved to {save_dir}legislation_pdf_urls.json")

        self.df_laws = pd.DataFrame(records)

    def get_report_text(self, report_url):

        report_url = self.normalize_url(report_url)
        try:
            print(f"Downloading {report_url}")
            response = requests.get(report_url, timeout=10)
            response.raise_for_status()
            pdf_stream = BytesIO(response.content)
            doc = fitz.open(stream=pdf_stream, filetype="pdf")
            text = ""
            for page in doc:
                text += page.get_text()

            # Use OCR if no extractable text
            if not text.strip():
                text = self.get_pdf_ocr(response.content)
            return text.strip()

        except Exception as e:
            print(f"Error downloading or extracting PDF: {e} for {report_url}")
            return None

    def get_pdf_ocr(self, pdf_bytes):
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(pdf_bytes)
            tmp_path = tmp_file.name

        try:
            pages = convert_from_path(tmp_path, poppler_path="/opt/homebrew/bin")  
            text = ""
            for page in pages:
                text += pytesseract.image_to_string(page)
            return text.strip()
        except Exception as e:
            print(f"OCR failed: {e}")
            return ""

    # This prevents errors for urls with accented character issues (e.g. Spanish, French, etc.)
    def normalize_url(self, url):
        base, filename = url.rsplit("/", 1)
        filename_nfc = unicodedata.normalize("NFC", filename)
        filename_encoded = urllib.parse.quote(filename_nfc)
        return f"{base}/{filename_encoded}"

    def get_country_laws(self, country):
        
        save_dir = "../../../data/raw/legislations"
        os.makedirs(save_dir, exist_ok=True)

        if self.df_laws is None:
            self.fetch_law_urls()

        df = self.df_laws
        df["Year-Month"] = df["Year-Month"].astype(str)

        if country in self.countries:
            country_df = df[df["Country/Institution"] == country].copy()
            if country_df.empty:
                return None
            
            print(f"Processing {country}")
            texts = []
            
            for pdf_url in country_df["pdf_url"]:
                text = self.get_report_text(pdf_url)
                texts.append(text)
                
            country_df["pdf_text"] = texts
            file_name = f"{country.replace(' ', '_').replace('/', '_')}.parquet"
            file_path = os.path.join(save_dir, file_name)
            country_df.to_parquet(file_path, index=False)
        
        else:
            print(f"No records found for {country}")
            return None
    
    def get_all_country_laws(self):

        for country in self.countries:
            self.get_country_laws(country)
            delay = random.uniform(3, 5)  
            time.sleep(delay)

    def get_country_parquet(self, country):

        base_dir = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "..", "..",
                "data", "raw", "legislations"
            )
        )
        file_name = f"{country.replace(' ', '_').replace('/', '_')}.parquet"
        file_path = os.path.join(base_dir, file_name)

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"No parquet file found for {country} at {file_path}")

        return pd.read_parquet(file_path)





            

