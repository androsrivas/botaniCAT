from dotenv import load_dotenv
import os
from botaniCAT.scraper.utils import scrape_paginated, clean_list_column
import pandas as pd


def get_usos_medicinals_df(save_csv=False):
    load_dotenv()

    base_url = os.environ.get('ETNOBOTANICA_BASE_URL')
    start_path = os.environ.get('ETNOBOTANICA_USOS_MEDICINALS_PATH')

    if not base_url or not start_path:
        raise ValueError(f"URL {base_url} or {start_path} not found")
    
    os.makedirs('data', exist_ok=True)

    all_rows = scrape_paginated(base_url, start_path)

    if not all_rows:
        print("No data collected")
        return pd.DataFrame(columns=['Familia', 'Tàxon', 'Usos medicinals'])
    
    df = pd.concat(all_rows, ignore_index=True)

    df_final = pd.DataFrame({
        'Familia' : df.iloc[:, 0],
        'Tàxon' : df.iloc[:, 1],
        'Usos medicinals' : df.iloc[:, 2].apply(clean_list_column)
    })

    if save_csv:
        df_final.to_csv('data/usos_medicinals.csv')
        print("CSV saved")

    return df_final