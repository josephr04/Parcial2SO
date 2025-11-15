"""
Modelo para gestionar las categorías en MySQL.
"""
import os
import mysql.connector
from mysql.connector import Error

def get_connection():
	host = os.getenv("MYSQL_HOST", "localhost")
	user = os.getenv("MYSQL_USER", "root")
	password = os.getenv("MYSQL_PASSWORD", "")

	database = os.getenv("MYSQL_DB", "restaurante")
	return mysql.connector.connect(host=host, user=user, password=password, database=database)

def init_db():
	"""Crea la tabla `categorias` si no existe."""
	conn = None

	try:
		conn = get_connection()
		cur = conn.cursor()
		cur.execute(
			"""
			CREATE TABLE IF NOT EXISTS categorias (
				id INT AUTO_INCREMENT PRIMARY KEY,
				nombre VARCHAR(255) NOT NULL,
				ruta_imagen VARCHAR(512)
			) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
			"""
		)

		conn.commit()
	finally:
		if conn and conn.is_connected():
			cur.close()
			conn.close()

def crear_categoria(nombre, ruta_imagen=None):
	"""Inserta una categoría y devuelve el id creado."""
	conn = get_connection()

	try:
		cur = conn.cursor()
		cur.execute("INSERT INTO categorias (nombre, ruta_imagen) VALUES (%s, %s)", (nombre, ruta_imagen))
		conn.commit()
		return cur.lastrowid
	finally:
		cur.close()
		conn.close()

def obtener_categorias():
	"""Devuelve una lista de tuplas (id, nombre, ruta_imagen)."""
	conn = get_connection()

	try:
		cur = conn.cursor()
		cur.execute("SELECT id, nombre, ruta_imagen FROM categorias ORDER BY id")
		return cur.fetchall()
	finally:
		cur.close()
		conn.close()

def obtener_categoria(id_):
	conn = get_connection()

	try:
		cur = conn.cursor()
		cur.execute("SELECT id, nombre, ruta_imagen FROM categorias WHERE id = %s", (id_,))
		return cur.fetchone()
	finally:
		cur.close()
		conn.close()

def actualizar_categoria(id_, nombre, ruta_imagen=None):
	conn = get_connection()

	try:
		cur = conn.cursor()
		cur.execute(
			"UPDATE categorias SET nombre = %s, ruta_imagen = %s WHERE id = %s",
			(nombre, ruta_imagen, id_),
		)
		conn.commit()
		return cur.rowcount
	finally:
		cur.close()
		conn.close()

def eliminar_categoria(id_):
	conn = get_connection()

	try:
		cur = conn.cursor()
		cur.execute("DELETE FROM categorias WHERE id = %s", (id_,))
		conn.commit()
		return cur.rowcount
	finally:
		cur.close()
		conn.close()

# Inicializar tabla al importar el módulo (silencioso en errores de conexión)
try:
	init_db()
except Exception:
	# Si no hay conexión o credenciales, no dejamos que la importación falle
	pass
