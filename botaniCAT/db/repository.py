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

def get_us(conn, description):
    cur = conn.cursor()
    cur.execute("SELECT id FROM Usos_medicinals WHERE description=?", (description,))
    row = cur.fetchone()
    return row[0] if row else None

def create_us(conn, description):
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO Usos_medicinals (description) VALUES (?)", (description,))
    conn.commit()
    return get_us(conn, description)

def link_plant_us(conn, plant_id, us_id):
    cur = conn.cursor()
    cur.execute(
        "INSERT OR IGNORE INTO Plant_usos (plant_id, us_id) VALUES (?, ?)",
        (plant_id, us_id)
    )
    conn.commit()
    
class Transaction:
    def __init__(self, conn):
        self.conn = conn

    def __enter__(self):
        return self.conn.cursor()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.conn.commit()
        else:
            self.conn.rollback()