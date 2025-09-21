import sqlite3
from botaniCAT.scraper.noms_populars import get_noms_populars_df

df_final = get_noms_populars_df(True)

conn = sqlite3.connect('data/botaniCAT.db')
cursor = conn.cursor()

for _, row in df_final.iterrows():
    cursor.execute("INSERT INTO Plants(family, taxon) VALUES (?, ?)", (row["Familia"], row["Tàxon"]))
    plant_id = cursor.lastrowid

    for nom in row["Noms populars"]:
        cursor.execute("INSERT INTO Noms_populars(name, plant_id) VALUES (?, ?)", (nom, plant_id))

conn.commit()
conn.close()
print("Data imported successfully to data/botaniCAT.db")

