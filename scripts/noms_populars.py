from bs4 import BeautifulSoup
from io import StringIO
from dotenv import load_dotenv
import os
import requests
import pandas as pd

load_dotenv()

base_url = os.environ.get('ETNOBOTANICA_BASE_URL')
start_path = os.environ.get('ETNOBOTANICA_NOMS_POPULARS_PATH')

if not base_url or not start_path:
    raise ValueError(f"URL {base_url} or {start_path} not found")

os.makedirs('data', exist_ok=True)

all_rows = []
next_url = base_url + start_path

    
while next_url:
    response = requests.get(next_url)
    if response.status_code != 200:
        print(f"Error {response.status_code}, stopping scraping")
        break

    html_data = response.text
    bs = BeautifulSoup(html_data, 'lxml')
    
    table = bs.find('table')
    
    if not table:
        print("Not table found, stopping.")
        break

    df = pd.read_html(StringIO((str(table))))[0]
    all_rows.append(df)
    print(f"Scraping {next_url}")

    next_link = bs.find('a', title="next")
    if next_link and 'href' in next_link.attrs:
        next_url = base_url + next_link['href']
    else:
        next_url = None

if all_rows:
    df = pd.concat(all_rows, ignore_index=True)
    
    families = df.iloc[:, 0]
    taxons = df.iloc[:, 1]

    # Function to split values in a list
    def separar_noms(x):
        if pd.isna(x):
            return[]
        return [v.strip() for v in x.split(',')]

    noms_populars = df.iloc[:, 2].apply(separar_noms) 

    df_final = pd.DataFrame({
        'Familia': families,
        'Tàxon' : taxons,
        'Noms populars' : noms_populars
    })

    df_final.to_csv('data/noms_populars.csv', index=False, encoding='utf-8')
    print("CSV saved")
else:
    print("No data collected")
