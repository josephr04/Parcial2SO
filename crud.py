# crud.py (Añadir este bloque si falta)
from database import conectar

# ===============================================
# CRUD para CATEGORÍAS
# ===============================================
def agregar_plato(nombre, descripcion, precio, categoria_id, imagen):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO platos (nombre, descripcion, precio, categoria_id, imagen)
        VALUES (?, ?, ?, ?, ?)
    """, (nombre, descripcion, precio, categoria_id, imagen))
    conn.commit()
    conn.close()


def obtener_platos():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT * FROM platos")
    platos = cur.fetchall()
    conn.close()
    return platos


def actualizar_plato(id_, nombre, descripcion, precio, categoria_id, imagen):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        UPDATE platos
        SET nombre = ?, descripcion = ?, precio = ?, categoria_id = ?, imagen = ?
        WHERE id = ?
    """, (nombre, descripcion, precio, categoria_id, imagen, id_))
    conn.commit()
    conn.close()


def eliminar_plato(id_):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("DELETE FROM platos WHERE id = ?", (id_,))
    conn.commit()
    conn.close()
