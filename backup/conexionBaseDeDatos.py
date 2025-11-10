# ============================================================================
# Script de Python para interactuar con la BBDD 'intertribus'
# ============================================================================

import mysql.connector
from mysql.connector import Error

# --- Módulo de Conexión ---
def crear_conexion():
    """Crea y devuelve un objeto de conexión a la base de datos."""
    try:
        conexion = mysql.connector.connect(
            host='localhost',
            user='root',
            password='', # <-- REEMPLAZAR
            database='intertribus'
        )
        if conexion.is_connected():            
            print("Conexión a 'intertribus' exitosa.")
            return conexion
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None
