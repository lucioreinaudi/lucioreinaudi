import mysql.connector
import pandas as pd
import random

# --- CONFIGURACIÓN DE LA BASE DE DATOS ---

DB_CONFIG = {
    'user': 'root', 
    'password': '',  
    'host': '127.0.0.1', 
    'database': 'intertribu1',
    'port': 3307  
}

# --- FUNCIONES DE UTILIDAD PARA LA BD ---

def conectar_bd():
    """Establece la conexión a la base de datos."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        print(f"Error al conectar a la BD: {err}")
        return None
