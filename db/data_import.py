import sqlite3
from scraper.noms_populars import get_df_final

df_final = get_df_final(True)

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

