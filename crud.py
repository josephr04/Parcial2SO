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

# ===============================================
# CRUD para PLATOS
# ===============================================

def agregar_plato(nombre, descripcion, precio, categoria_id, imagen):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO platos (nombre, descripcion, precio, id_categoria, ruta_imagen)
        VALUES (%s, %s, %s, %s, %s)
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
        SET nombre = %s, descripcion = %s, precio = %s, id_categoria = %s, ruta_imagen = %s
        WHERE id = %s
    """, (nombre, descripcion, precio, categoria_id, imagen, id_))
    conn.commit()
    conn.close()

def eliminar_plato(id_):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("DELETE FROM platos WHERE id = %s", (id_,))
    conn.commit()
    conn.close()

def existe_plato(nombre):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM platos WHERE LOWER(nombre) = LOWER(%s)", (nombre,))
    existe = cur.fetchone()[0] > 0
    conn.close()
    return existe
