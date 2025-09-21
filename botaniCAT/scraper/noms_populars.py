from dotenv import load_dotenv
import os
from botaniCAT.scraper.utils import scrape_paginated, clean_list_column
import pandas as pd

def get_noms_populars_df(save_csv=False):
    load_dotenv()

    base_url = os.environ.get('ETNOBOTANICA_BASE_URL')
    start_path = os.environ.get('ETNOBOTANICA_NOMS_POPULARS_PATH')

    if not base_url or not start_path:
        raise ValueError(f"URL {base_url} or {start_path} not found")

    os.makedirs('data', exist_ok=True)

    all_rows = scrape_paginated(base_url, start_path)

    if not all_rows:
        print("No data collected")
        return pd.DataFrame(columns=['Familia', 'Tàxon', 'Noms populars'])
    
    df = pd.concat(all_rows, ignore_index=True)

    df_final = pd.DataFrame({
            'Familia': df.iloc[:, 0],
            'Tàxon' : df.iloc[:, 1],
            'Noms populars' : df.iloc[:, 2].apply(clean_list_column)
        })
    
    if save_csv:
        df_final.to_csv('data/noms_populars.csv', index=False, encoding='utf-8')
        print("CSV saved")

    return df_final
        