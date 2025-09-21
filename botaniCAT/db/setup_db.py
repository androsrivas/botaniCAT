import sqlite3

with sqlite3.connect('data/botaniCAT.db') as conn:
    cursor = conn.cursor()
    print("Database created and connected successfully!")

    create_plant_table_query = '''
    CREATE TABLE IF NOT EXISTS Plants (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        family TEXT NOT NULL,
        taxon TEXT NOT NULL
    );
    '''
    cursor.execute(create_plant_table_query)

    create_noms_populars_table_query = '''
    CREATE TABLE IF NOT EXISTS Noms_populars (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        plant_id INTEGER NOT NULL,
        FOREIGN KEY (plant_id) REFERENCES Plants(id) ON DELETE CASCADE
    );
    '''
    cursor.execute(create_noms_populars_table_query)

    create_usos_medicinals_table_query = '''
    CREATE TABLE IF NOT EXISTS Usos_medicinals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        description TEXT NOT NULL,
        plant_id INTEGER NOT NULL,
        FOREIGN KEY (plant_id) REFERENCES Plants(id) ON DELETE CASCADE
    );
    '''
    cursor.execute(create_usos_medicinals_table_query)

    conn.commit()
    print("Tables created successfully!")
