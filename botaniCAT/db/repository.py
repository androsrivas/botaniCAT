import sqlite3

def get_connection(db_path="data/botaniCAT.db"):
    return sqlite3.connect(db_path)

def get_plant(conn, family, taxon):
    cur = conn.cursor()
    cur.execute("SELECT id FROM Plants WHERE family=? AND taxon=?", (family, taxon))
    row = cur.fetchone()
    return row[0] if row else None

def create_plant(conn, family, taxon):
    cur = conn.cursor()
    cur.execute("INSERT INTO Plants (family, taxon) VALUES (?, ?)", (family, taxon))
    conn.commit()
    return cur.lastrowid

def get_or_create_plant(conn, family, taxon):
    plant_id = get_plant(conn, family, taxon)
    if plant_id:
        return plant_id
    return create_plant(conn, family, taxon)

def insert_nom_popular(conn, name, plant_id):
    cur = conn.cursor()
    cur.execute("INSERT INTO Noms_populars (name, plant_id) VALUES (?, ?)", (name, plant_id))
    conn.commit()

def insert_us_medicinal(conn, description, plant_id):
    cur = conn.cursor()
    cur.execute("INSERT INTO Usos_medicinals (description, plant_id) VALUES (?, ?)", (description, plant_id))
    conn.commit()