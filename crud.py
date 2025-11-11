# crud.py (Añadir este bloque si falta)
from database import conectar

# ===============================================
# CRUD para CATEGORÍAS
# ===============================================

def obtener_categorias():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT id, nombre FROM categorias")
    categorias = cur.fetchall()
    conn.close()
    return categorias


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
    cur.execute("""
        SELECT 
            p.id,
            p.nombre,
            p.descripcion,
            p.precio,
            c.nombre AS categoria,
            p.ruta_imagen
        FROM platos p
        LEFT JOIN categorias c ON p.id_categoria = c.id
    """)
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
