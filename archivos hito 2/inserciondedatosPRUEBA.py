import mysql.connector
import pandas as pd
import random

# --- CONFIGURACIÓN DE LA BASE DE DATOS ---
# NOTA: Debes reemplazar estos valores con tus credenciales reales
DB_CONFIG = {
    'user': 'root', 
    'password': '',  # Probablemente tu contraseña si tienes una configurada
    'host': '127.0.0.1', 
    'database': 'intertribus1 (2)',
    'port': 3306  # El puerto que indicaste en tu script
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
    
import mysql.connector
from mysql.connector import Error

# --- Módulo de Conexión (usando la base 'intertribu1' y la contraseña vacía) ---
def crear_conexion():
    """Crea y devuelve un objeto de conexión a la base de datos."""
    try:
        conexion = mysql.connector.connect(
            host='localhost',
            user='root',
            password='', 
            database='intertribus1 (2)' # <-- Base de datos de tu SQL Dump
        )
        if conexion.is_connected():          
            print("Conexión a 'intertribu1' exitosa.")
            return conexion
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

# --- Función de Inserción ---
def inscribir_estudiante(estudiante_id, actividad_id):
    """
    Inserta un nuevo registro en la tabla 'inscripciones' usando los IDs dados.
    """
    conexion = crear_conexion()
    if conexion is None:
        return

    try:
        cursor = conexion.cursor()
        
        # 1. Sentencia SQL de INSERCIÓN
        # La columna idinscripciones se autoincrementa, así que solo pasamos los dos FK.
        sql_insert = """
            INSERT INTO inscripciones (idEstudiante, idActividad) 
            VALUES (%s, %s)
        """
        
        # 2. Datos a insertar (como una tupla)
        datos = (estudiante_id, actividad_id)
        
        # 3. Ejecutar la inserción
        cursor.execute(sql_insert, datos)
        
        # 4. Confirmar los cambios
        conexion.commit()
        
        # Opcional: Obtener el ID que se autogeneró (idinscripciones)
        nueva_inscripcion_id = cursor.lastrowid
        
        print("\n==============================================")
        print(f"✅ ¡Inscripción realizada con éxito!")
        print(f"Estudiante ID: {estudiante_id} inscrito en Actividad ID: {actividad_id}")
        print(f"ID de Inscripción generado: {nueva_inscripcion_id}")
        print("==============================================")


    except mysql.connector.Error as e:
        # Esto captura errores como si el Estudiante ID o Actividad ID no existen (FK error)
        print(f"\n❌ Error al intentar inscribir: {e}")
        if conexion.is_connected():
            conexion.rollback() # Deshace el cambio si hubo un error
    
    finally:
        # 5. Cerrar la conexión
        if conexion and conexion.is_connected():
            cursor.close()
            conexion.close()
            print("Conexión cerrada.")

# --- EJEMPLO DE USO ---

# Queremos inscribir al Estudiante con ID 10 ("Lucía Sosa" - Biología)
# en la Actividad con ID 1005 ("Volley").

# Revisa tu dump: 
# Estudiante ID 10 existe.
# Actividad ID 1005 existe.

inscribir_estudiante(10, 1005)

# Otro ejemplo: Estudiante ID 50 ("Isabella Ruiz" - Matemática)
# en la Actividad ID 1010 ("Truco").
inscribir_estudiante(50, 1010)

# Ejemplo de error (si intentas inscribir con un ID que NO existe)
# inscribir_estudiante(999, 1001)
