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

def mostrar_mini_menu_guardar():
    """Muestra el mini-menú después del sorteo."""
    print("\n" + "-" * 40)
    print("  OPCIONES POST-SORTEO")
    print("-" * 40)
    print("1 - Guardar equipos en la base de datos")
    print("0 - Volver al menú principal")
    print("-" * 40)

def ejecutar_opcion(opcion):
    """Ejecuta la acción correspondiente a la opción seleccionada."""
    global ultimo_resultado_sorteo
    
    if opcion == '1':
        conn = conectar_bd()
        if conn:
            mostrarInscripciones(conn)
            conn.close()
        else:
            print("No se pudo conectar a la base de datos para mostrar los inscritos.")
            
    elif opcion == '2':
        conn = conectar_bd()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT nombreActividad FROM actividad ORDER BY nombreActividad")
                actividades = [row[0] for row in cursor.fetchall()]
                print("\n--- LISTA DE ACTIVIDADES ---")
                for act in actividades:
                    print(f"- {act}")
            except Exception as e:
                print(f"Error al obtener actividades: {e}")
            finally:
                cursor.close()
                conn.close()
        else:
            print("No se pudo conectar a la base de datos para mostrar las actividades.")
            
    elif opcion == '3':
        conn = conectar_bd() 
        if conn is None:
            return

        df_inscripciones = obtener_datos_inscripciones(conn)
        conn.close()
        
        if df_inscripciones.empty:
            print("¡ERROR! No se encontraron inscripciones. La tabla está vacía o hay un error de lectura.")
            return

        actividades_disponibles = df_inscripciones['nombreActividad'].unique().tolist()
        print(f"Actividades a sortear: {actividades_disponibles}")

        cupos = obtenerCupos(actividades_disponibles)
        
        resultados = realizarSorteos(df_inscripciones, cupos)
        
        actividades_ordenadas_reporte = actividades_disponibles
        
        mostrarResultados(resultados, actividades_ordenadas_reporte, cupos)
        
        ultimo_resultado_sorteo = resultados
        
        while True:
            mostrar_mini_menu_guardar()
            opcion_guardar = input("Seleccione una opción: ").strip()
            
            if opcion_guardar == '1':
                guardarResultadosSQL(ultimo_resultado_sorteo)
                break 
            elif opcion_guardar == '0':
                print("Volviendo al menú principal...")
                break
            else:
                print("Opción no válida. Por favor, ingrese '1' o '0'.")
        
    elif opcion == '0':
        print("Saliendo del programa. ¡Hasta pronto!")
        return True 
        
    else:
        print("Opción no válida. Por favor, ingrese un número del 0 al 3.")
        
    return False

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
