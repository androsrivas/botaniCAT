from bs4 import BeautifulSoup
from io import StringIO
import os
import requests
import pandas as pd

# Read env var
url = os.environ.get('ETNOBOTANICA_NOMS_POPULARS_URL')
if not url:
    raise ValueError(f"URL {url} not found")

# Create output folder
os.makedirs('data', exist_ok=True)

# Request
response = requests.get(url)
if response.status_code != 200:
    raise Exception(f"Error fetching URL: {response.status_code}")

html_data = response.text
print("HTML successfully obtained")

# Scrapping
bs = BeautifulSoup(html_data, 'lxml')

table = bs.find('table')
html_string = str(table)

# Convert to DF
df = pd.read_html(StringIO(html_string))[0]

families = df.iloc[:, 0]
taxons = df.iloc[:, 1]

# Function to split values in a list
def separar_noms(x):
    if pd.isna(x):
        return[]
    return [v.strip() for v in x.split(',')]

noms_populars = df.iloc[:, 2].apply(separar_noms) 

# TODO: surpass pagination

# Final DF
df_final = pd.DataFrame({
    'Familia': families,
    'Tàxon' : taxons,
    'Noms populars' : noms_populars
})

# Export to CSV
df_final.to_csv('data/noms_populars.csv', index=False, encoding='utf-8')
