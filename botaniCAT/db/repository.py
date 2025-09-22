import sqlite3

# Connection
def get_connection(db_path="data/botaniCAT.db"):
    return sqlite3.connect(db_path)

# CRUD

# Plants
def get_plant_by_id(conn, plant_id):
    cur = conn.cursor()
    cur.execute("SELECT id FROM Plants WHERE plant_id=?", (plant_id))
    row = cur.fetchone()
    return row[0] if row else None

def get_plant_by_family_and_taxon(conn, family, taxon):
    cur = conn.cursor()
    cur.execute("SELECT id FROM Plants WHERE family=? AND taxon=?", (family, taxon))
    row = cur.fetchone()
    return row[0] if row else None

def create_plant(conn, family, taxon):
    cur = conn.cursor()
    cur.execute("INSERT INTO Plants (family, taxon) VALUES (?, ?)", (family, taxon))
    conn.commit()
    return cur.lastrowid

def insert_plant_image(conn, plant_id, image_url, public_id=None):
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO Plant_images (plant_id, image_url, image_public_id) VALUES (?, ?, ?)",
        (plant_id, image_url, public_id)
    )

def get_or_create_plant(conn, family, taxon):
    plant_id = get_plant_by_family_and_taxon(conn, family, taxon)
    if plant_id:
        return plant_id
    return create_plant(conn, family, taxon)

# Noms populars
def insert_nom_popular(conn, name, plant_id):
    cur = conn.cursor()
    cur.execute("INSERT INTO Noms_populars (name, plant_id) VALUES (?, ?)", (name, plant_id))
    conn.commit()

# Usos medicinals
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
    

# Transaction 
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