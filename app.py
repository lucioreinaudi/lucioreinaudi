import mysql.connector
import pandas as pd
import random

# --- CONFIGURACIÓN DE LA BASE DE DATOS ---
# NOTA: Debes reemplazar estos valores con tus credenciales reales
DB_CONFIG = {
    'user': 'root', 
    'password': '',  # Probablemente tu contraseña si tienes una configurada
    'host': '127.0.0.1', 
    'database': 'intertribu1',
    'port': 3307  # El puerto que indicaste en tu script
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

def obtener_datos_inscripciones(conn):
    """
    Obtiene y combina los datos de inscripciones, estudiantes y actividades
    en un único DataFrame de Pandas.
    """
    query = """
    SELECT 
        e.idestudiantes, 
        e.nombre, 
        e.apellido, 
        e.genero, 
        e.tribu,
        a.nombreActividad
    FROM 
        inscripciones i
    JOIN 
        estudiantes e ON i.idEstudiante = e.idestudiantes
    JOIN 
        actividad a ON i.idActividad = a.idactividad;
    """
    try:
        # Usar Pandas para leer directamente desde la consulta SQL
        df = pd.read_sql(query, conn)
        return df
    except Exception as e:
        print(f"Error al obtener datos de la BD: {e}")
        # Retorna un DataFrame vacío si hay error o si no hay inscripciones
        return pd.DataFrame()
    
def obtenerCupos(actividadesDisponibles):
    cupos= {}
    print("--- INGRESO DE CUPOS POR ACTIVIDAD ---")
    for actividad in actividadesDisponibles:
        while True:
            try:
                cupo = int(input(f"Ingrese cupo de participante por equipo de la actividad {actividad}"))   
                if cupo > 0:
                    cupos[actividad] = cupo
                    break
                else:
                    print("El cupo debe ser un numero positivo")
            except ValueError:
                print(f"Entrada no válida. Por favor, ingrese un numero entero")
    return cupos

def realizarSorteos(inscripciones, cupos):
    resultados={
        'equipos':{},
        'excluidos':{},
        'actividades_canceladas':[]
    }

    actividades = inscripciones['nombreActividad'].unique()
    for actividad in actividades:
        if actividad not in cupos:
            print(f"Advertencia: No se ingresó cupo para {actividad}")
            continue
        cupo_total = cupos[actividad]
        df_actividad = inscripciones[inscripciones['nombreActividad'] ==actividad].copy()

        grupos = df_actividad.groupby(['tribu','genero'])

        cupo_por_grupo = cupo_total // 4
        grupos_a_seleccionar = {}
        
        for (tribu, genero), df_grupo in grupos:
            max_a_seleccionar = min(cupo_por_grupo, len(df_grupo))
            grupos_a_seleccionar[(tribu,genero)] = max_a_seleccionar

            minimo_requerido = 1
            if any(cant < minimo_requerido for cant in grupos_a_seleccionar.values()):   
                resultados['actividades_canceladas'].append(f"{actividad} (Faltan inscritos en algún grupo: {grupos_a_seleccionar})")
                continue    

            equipos_seleccionado = pd.DataFrame()

            for(tribu, genero), df_grupo in grupos:
                n_seleccionar = grupos_a_seleccionar[(tribu,genero)]
            seleccion = df_grupo.sample(n=n_seleccionar, random_state=42)
            equipo_seleccionado = pd.concat([equipo_seleccionado, seleccion])
        
            ids_seleccionados = equipos_seleccionado['idestudiantes'].tolist()

            excluidos = actividad[actividad['idestudiantes'].isin(ids_seleccionados)]
    
            resultados['equipos'][actividad] = equipo_seleccionado
            resultados['excluidos'][actividad] = excluidos
    return resultados

def mostrarResultados(resultados):
    print("\n" + "=" *80)
    print(" RESULTADOS DEL SORTEO INTERTRIBU")
    print("=" * 80)

    print(" --- EQUIPOS CONFORMADOS (SELECCIONADOS) ---")
    for actividad, equipo in resultados['equipos'].items():
        print(f" ACTIVIDAD: {actividad.upper()} (Total: {len(equipo)})")

        conteo_equipo = equipo.groupby(['tribu', 'genero']).size().to_dict()
        print(f" -> Distribución:{conteo_equipo}")
        for index, row in equipo.iterrows():
            print(f"   - {row['nombre']} {row['apellido']} ({row['tribu']}, {row['genero']}) - Carrera: {row['carrera']}")
            print("-" * 20)    
        
    print ("--- ALUMNOS NO SELECCIONADOS (EXCLUIDOS POR CUPOS)")  
    total_excluidos = sum(len(df) for df in resultados['excluidos'].values())
    if total_excluidos > 0:
        for actividad, excluidos in resultados['excluidos'].items():
            if not excluidos.empty:
                print(f"ACTIVIDAD: {actividad.upper()} (Total Excluidos: {len(excluidos)})")
                for index, row in excluidos.iterrows():
                    print(f"   - {row['nombre']} {row['apellido']} ({row['tribu']}, {row['genero']})")
    else:
        print(f"¡No quedaron alumnos excluidos por cupo en las actividades sorteadas!")

    print(" --- ACTIVIDADES CANCELADAS ---")
    if resultados['actividades_canceladas']:
        for msg in resultados['actividades_canceladas']:
            print(f"    -{msg}")
    else:
        print("   - Todas las actividades sorteadas cumplen el mínimo de inscritos.")
    print("\n" + "="*80)

# --- FUNCIÓN PRINCIPAL ---

def main():
    """Función principal del programa."""
    conn = conectar_bd()
    if conn is None:
        return

    # 1. Obtener la información de la BD
    df_inscripciones = obtener_datos_inscripciones(conn)
    conn.close()

    if df_inscripciones.empty:
        print("🛑 ¡ERROR! No se encontraron inscripciones en la base de datos.")
        print("Asegúrate de haber llenado la tabla 'inscripciones' antes de ejecutar el sorteo.")
        return

    # 2. Obtener la lista de actividades y solicitar cupos
    actividades_disponibles = df_inscripciones['nombreActividad'].unique().tolist()
    print(f"Actividades a sortear: {actividades_disponibles}")
    
    cupos = obtenerCupos(actividades_disponibles)
    
    # 3. Realizar el sorteo
    resultados = realizarSorteos(df_inscripciones, cupos)
    
    # 4. Mostrar la salida requerida
    mostrarResultados(resultados)

if __name__ == "__main__":
    main()