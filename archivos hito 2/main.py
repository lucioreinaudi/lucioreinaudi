import pymysql.cursors
import pandas as pd
import random
import sqlalchemy 
from datetime import date 

DB_CONFIG = {
    'user': 'root', 
    'password': '',
    'host': '127.0.0.1', 
    'database': 'intertribu1',
    'port': 3307, 
    'connect_timeout': 5,
    'charset': 'utf8mb4' 
}


def conectar_bd():
    """Establece la conexión a la base de datos usando pymysql."""
    try:
        conn = pymysql.connect(
            user=DB_CONFIG['user'], 
            password=DB_CONFIG['password'], 
            host=DB_CONFIG['host'], 
            database=DB_CONFIG['database'], 
            port=DB_CONFIG['port'],
            connect_timeout=DB_CONFIG['connect_timeout'],
            charset=DB_CONFIG['charset']
        )
        return conn
    except Exception as err:
        print(f"ERROR DE CONEXIÓN! Detalles (pymysql): {err}")
        return None

def mostrar_menu():
    """Muestra el menú de opciones."""
    print("\n" + "=" * 40)
    print("      MENÚ SORTEO INTERTRIBU")
    print("=" * 40)
    print("1 - Mostrar inscritos")
    print("2 - Mostrar actividades")
    print("3 - Ingresar cupos y realizar sorteo")
    print("0 - Salir")
    print("-" * 40)

def main():
    """Función principal del programa que ejecuta el menú."""
    
    conn_temp = conectar_bd()
    if conn_temp:
        cursor = conn_temp.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM inscripciones")
            cantidad = cursor.fetchone()[0]
            if cantidad == 0:
                print("\nLa tabla 'inscripciones' está vacía. Debe agregar datos para sortear (Opción 3).")
            else:
                print(f"\nLa tabla 'inscripciones' tiene {cantidad} inscripciones listas para el sorteo.")
        except Exception:
            print("\nAdvertencia: No se pudo verificar el número de inscripciones.")
        finally:
            cursor.close()
            conn_temp.close()
    
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()
        
        if ejecutar_opcion(opcion):
            break

if __name__ == "__main__":
    main()
