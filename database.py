import sqlite3

def conectar():
    conn = sqlite3.connect("restaurante.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS platos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            precio REAL NOT NULL,
            categoria_id INTEGER,
            imagen TEXT
    
    """)
    conn.commit()
    return conn

