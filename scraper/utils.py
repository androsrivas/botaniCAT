from bs4 import BeautifulSoup
from io import StringIO
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