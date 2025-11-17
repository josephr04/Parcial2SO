import mysql.connector
from mysql.connector import Error

def conectar():
    try:
        conn = mysql.connector.connect(
            host="localhost",       
            user="root",            
            password="",            
            database="restaurante"  
        )
        if conn.is_connected():
            return conn
    except Error as e:
        print("Error al conectar:", e)
        return None
