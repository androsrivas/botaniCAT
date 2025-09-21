from botaniCAT.scraper.noms_populars import get_noms_populars_df
from botaniCAT.scraper.usos_medicinals import get_usos_medicinals_df
from botaniCAT.db.repository import(
    get_connection,
    get_or_create_plant,
    insert_nom_popular,
    get_us,
    create_us,
    link_plant_us,
    Transaction
)

def import_data():
    conn = get_connection()

    df_names = get_noms_populars_df(True)
    df_uses = get_usos_medicinals_df(True)

    with Transaction(conn) as cur:
        for _, row in df_names.iterrows():
            plant_id = get_or_create_plant(conn, row["Familia"], row["Tàxon"])
            for name in row["Noms populars"]:
                insert_nom_popular(conn, name, plant_id)

        for _, row in df_uses.iterrows():
            plant_id = get_or_create_plant(conn, row["Familia"], row["Tàxon"])
            for use in row["Usos medicinals"]:
                use_id = create_us(conn, use)
                link_plant_us(conn, plant_id, use_id)

    conn.close()
    print("Data imported successfully to data/botaniCAT.db")

if __name__ == "__main__":
    import_data()