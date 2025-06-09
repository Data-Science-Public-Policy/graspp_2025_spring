import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
src_path = os.path.join(project_root, "src")
sys.path.append(src_path)

from download_genealogies import download_genealogies
from transform_genealogies import transform_genealogy_data

#Step 1: Download genealogy data
download_genealogies(
    start_page=1,
    num_pages=5160,
    chromedriver_path=os.path.join(project_root, "tools", "chromedriver-win64", "chromedriver.exe"),
    output_dir=os.path.join(project_root, "data")
)

#Step 2: Transform raw data into panel format
input_path = os.path.join(project_root, "data", "data_raw_genealogy_En.csv")
output_path = os.path.join(project_root, "data", "genealogy_panel.csv")

transform_genealogy_data(input_path=input_path, output_path=output_path)






