from bs4 import BeautifulSoup
from io import StringIO
import requests
import pandas as pd
import re

def fetch_table(response_text):
    bs = BeautifulSoup(response_text, "lxml")
    table = bs.find("table")
    if not table:
        return None
    return pd.read_html(StringIO(str(table)))[0]

def clean_list_column(cell_value):
    if pd.isna(cell_value):
        return[]
    values = [v.strip() for v in cell_value.split(",")]
    clean_values = [re.sub(r"\(.*?\)", "", value).strip() for value in values]
    return [cv for cv in clean_values if cv]

def scrape_paginated(base_url, start_path, next_selector="a[title='next']"):
    all_rows = []
    next_url = base_url + start_path

    while next_url:
        response = requests.get(next_url)
        if response.status_code != 200:
            print(f"Error {response.status_code} a {next_url}")
            break
        
        df = fetch_table(response.text)
        if df is not None:
            all_rows.append(df)
            print(f"Scraped {next_url}")
        else:
            print(f"No table found in {next_url}")
            break

        bs = BeautifulSoup(response.text, "lxml")
        next_links = bs.select(next_selector)
        
        if next_links:
            next_link = next_links[0]
            href = next_link.get('href')
            if href:
                next_url = base_url + href
            else:
                next_url = None
        else:
            next_url = None

    return all_rows