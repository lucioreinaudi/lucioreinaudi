import pymysql.cursors
import pandas as pd
import random
import sqlalchemy 
from reporteDeAgregacion import tablaIinscripcionesVacia
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

def mostrarInscripciones(conexion):
    """Muestra los inscriptos detallados con formato de tabla."""
    cursor = conexion.cursor()
    consulta = """
        SELECT e.nombre, e.apellido, e.tribu, e.genero, a.nombreActividad
        FROM inscripciones i
        JOIN estudiantes e ON i.idEstudiante = e.idestudiantes
        JOIN actividad a ON i.idActividad = a.idactividad
        ORDER BY a.nombreActividad, e.tribu, e.genero
    """
    cursor.execute(consulta)
    resultados = cursor.fetchall()

    print("\n" + "=" * 80)
    print(f"{'NOMBRE COMPLETO':<25} | {'TRIBU Y GÉNERO':^18} | {'ACTIVIDAD':<30}")
    print("=" * 80)

    for fila in resultados:
        nombre_completo = f"{fila[0]} {fila[1]}"
        tribu_genero = f"Tribu {fila[2]} ({fila[3]})" 
        
        print(
            f"{nombre_completo:<25} | {tribu_genero:^18} | {fila[4]:<30}"
        )
    
    print("=" * 80)
    cursor.close()

def obtener_datos_inscripciones(conn):
    """Obtiene y combina los datos de inscripciones, estudiantes y actividades en un DataFrame."""
    query = """
    SELECT 
        e.idestudiantes, 
        e.nombre, 
        e.apellido, 
        e.carrera,           
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
        db_url = (
            f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@"
            f"{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
        )

        dtype_map = {col: str for col in ['idestudiantes', 'nombre', 'apellido', 'carrera', 'genero', 'tribu', 'nombreActividad']}
        df = pd.read_sql(query, db_url, dtype=dtype_map)

        str_cols = ['nombre', 'apellido', 'carrera', 'genero', 'tribu', 'nombreActividad']
        for col in str_cols:
            if col in df.columns:
                df[col] = df[col].str.strip() 

        df = df[df['nombre'] != 'nombre']
        df = df[df['nombreActividad'] != 'nombreActividad']

        return df
        
    except Exception as e: 
        return pd.DataFrame()

def obtenerCupos(actividadesDisponibles):
    """Solicita al usuario el cupo por equipo para cada actividad."""
    cupos= {}
    print("--- INGRESO DE CUPOS POR ACTIVIDAD ---")
    for actividad in actividadesDisponibles:
        while True:
            try:
                cupo_str = input(f"Ingrese cupo de participante por equipo de la actividad {actividad}: ")
                cupo = int(cupo_str)
                if cupo > 0:
                    cupos[actividad] = cupo
                    break
                else:
                    print("El cupo debe ser un número positivo.")
            except ValueError:  
                print(f"Entrada no válida. Por favor, ingrese un número entero.")
    return cupos

def realizarSorteos(inscripciones, cupos):
    """
    Realiza el sorteo, garantizando la paridad de Tribu y Género, 
    dividiendo el cupo total entre los dos equipos finales (Azul y Verde).
    """
    resultados = {
        'equipos': {},
        'excluidos': {},
        'actividades_canceladas': []
    }
    
    actividades = inscripciones['nombreActividad'].unique()
    MINIMO_REQUERIDO_POR_SUBGRUPO = 1 

    for actividad in actividades:
        if actividad not in cupos:
            continue
            
        cupo_por_equipo_ingresado = cupos[actividad]
        
        df_actividad = inscripciones[inscripciones['nombreActividad'] == actividad].copy()

        grupos = df_actividad.groupby(['tribu', 'genero'])
        
        cupo_azul = cupo_por_equipo_ingresado
        cupo_verde = cupo_por_equipo_ingresado

        grupos_a_seleccionar = {}
        minimo_inscritos_cumplido = True
        
        for (tribu, genero), df_grupo in grupos:
            
            if len(df_grupo) < MINIMO_REQUERIDO_POR_SUBGRUPO:
                 minimo_inscritos_cumplido = False
                 break 
            
            cupo_tribu = cupo_azul if tribu == 'Azul' else cupo_verde
            cupo_deseado_subgrupo = cupo_tribu // 2 
            
            n_seleccionar = min(cupo_deseado_subgrupo, len(df_grupo))
            grupos_a_seleccionar[(tribu, genero)] = n_seleccionar
            
        if not minimo_inscritos_cumplido:
            grupos_dist = grupos.size().to_dict()
            resultados['actividades_canceladas'].append(
                f"{actividad} (CANCELADA - Falta el mínimo (1) de inscritos en un subgrupo T/G. Distribución: {grupos_dist})"
            )
            continue
            
        equipo_azul = pd.DataFrame()
        equipo_verde = pd.DataFrame()
        
        for (tribu, genero), df_grupo in grupos:
            n_seleccionar = grupos_a_seleccionar[(tribu, genero)]
            
            if n_seleccionar == 0:
                continue

            seleccion = df_grupo.sample(n=n_seleccionar, random_state=42) 
            
            if tribu == 'Azul':
                equipo_azul = pd.concat([equipo_azul, seleccion], ignore_index=True)
            else:
                equipo_verde = pd.concat([equipo_verde, seleccion], ignore_index=True)
            
        equipo_seleccionado = pd.concat([equipo_azul, equipo_verde], ignore_index=True)
            
        if equipo_seleccionado.empty:
            ids_seleccionados = []
            excluidos = df_actividad.copy() 
        else:
            ids_seleccionados = equipo_seleccionado['idestudiantes'].tolist()
            excluidos = df_actividad[~df_actividad['idestudiantes'].isin(ids_seleccionados)].copy()
        
        resultados['equipos'][f"{actividad} (AZUL)"] = equipo_azul
        resultados['equipos'][f"{actividad} (VERDE)"] = equipo_verde
        resultados['excluidos'][actividad] = excluidos
        
    return resultados

def mostrarResultados(resultados, actividades_ordenadas_reporte, cupos_ingresados):
    """Imprime los resultados del sorteo en la terminal, incluyendo mensajes de cupo incompleto con el número faltante."""
    print("\n" + "=" *80)
    print(" RESULTADOS DEL SORTEO INTERTRIBU")
    print("=" * 80)

    print(" --- EQUIPOS CONFORMADOS (SELECCIONADOS) ---")
    if resultados['equipos']:
        
        for actividad_base in actividades_ordenadas_reporte:
            cupo_requerido = cupos_ingresados.get(actividad_base, 0) 
            
            print(f"\n--- ACTIVIDAD: {actividad_base.upper()} ---")
            print("=" * 35)
            
            clave_azul = f"{actividad_base} (AZUL)"
            if clave_azul in resultados['equipos']:
                equipo = resultados['equipos'][clave_azul]
                total_seleccionado = len(equipo)
                print(f" EQUIPO AZUL (Total: {total_seleccionado})")
                
                if total_seleccionado < cupo_requerido:
                    faltantes = cupo_requerido - total_seleccionado
                    print(f"No se completó el equipo por falta de inscriptos. Faltan {faltantes} cupos.")
                
                if not equipo.empty:
                    conteo_equipo = equipo.groupby(['genero']).size().to_dict()
                    print(f" -> Distribución (GÉNERO): {conteo_equipo}")
                    print(" Seleccionados:")
                    for index, row in equipo.iterrows():
                        print(f"   - {row['nombre']} {row['apellido']} ({row['genero']}) - Carrera: {row['carrera']}")
                else:
                    print(" -> Distribución (GÉNERO): {}")
                    print(" Seleccionados: (No se pudo formar el equipo completo de la Tribu Azul)")
                print("-" * 35)
                
            clave_verde = f"{actividad_base} (VERDE)"
            if clave_verde in resultados['equipos']:
                equipo = resultados['equipos'][clave_verde]
                total_seleccionado = len(equipo)
                print(f" EQUIPO VERDE (Total: {total_seleccionado})")
                
                if total_seleccionado < cupo_requerido:
                    faltantes = cupo_requerido - total_seleccionado
                    print(f"No se completó el equipo por falta de inscriptos. Faltan {faltantes} cupos.")

                if not equipo.empty:
                    conteo_equipo = equipo.groupby(['genero']).size().to_dict()
                    print(f" -> Distribución (GÉNERO): {conteo_equipo}")
                    print(" Seleccionados:")
                    for index, row in equipo.iterrows():
                        print(f"   - {row['nombre']} {row['apellido']} ({row['genero']}) - Carrera: {row['carrera']}")
                else:
                    print(" -> Distribución (GÉNERO): {}")
                    print(" Seleccionados: (No se pudo formar el equipo completo de la Tribu Verde)")
                print("-" * 80)

    else:
        print("No se pudo conformar ningún equipo.")
        
    print ("--- ALUMNOS NO SELECCIONADOS---") 
    total_excluidos = sum(len(df) for df in resultados['excluidos'].values())
    if total_excluidos > 0:
        for actividad, excluidos in resultados['excluidos'].items():
            if not excluidos.empty:
                print(f"ACTIVIDAD: {actividad.upper()} (Total Excluidos: {len(excluidos)})")
                
                for index, row in excluidos.iterrows():
                    print(f"   - {row['nombre']} {row['apellido']} ({row['tribu']}, {row['genero']})")
                print("-" * 80)
    else:
        print(f"¡No quedaron alumnos excluidos por cupo en las actividades sorteadas!")

    print(" --- ACTIVIDADES CANCELADAS ---")
    if resultados['actividades_canceladas']:
        for msg in resultados['actividades_canceladas']:
            print(f"   - {msg}")
    else:
        print("   - Todas las actividades sorteadas cumplen el mínimo de inscritos.")
    print("\n" + "="*80)

def guardarResultadosSQL(resultados):
    """Guarda los equipos seleccionados en la tabla 'resultados_sorteo'."""
    conexion = conectar_bd()
    if not conexion:
        print("Error: No se pudo conectar a la BD para guardar los resultados.")
        return

    cursor = conexion.cursor()
    fecha_actual = date.today()
    exitosos = 0
    
    try:
        for clave, df_equipo in resultados['equipos'].items():
            if df_equipo.empty:
                continue

            actividad_nombre = clave.split(' (')[0].strip()
            tribu_equipo = clave.split(' (')[1].replace(')', '').strip()

            cursor.execute("SELECT idactividad FROM actividad WHERE nombreActividad = %s", (actividad_nombre,))
            actividad_id = cursor.fetchone()
            
            if not actividad_id:
                print(f"Advertencia: ID de actividad no encontrado para '{actividad_nombre}'. Saltando.")
                continue
            
            actividad_id = actividad_id[0]

            valores = []
            for index, row in df_equipo.iterrows():
                valores.append((
                    row['idestudiantes'], 
                    actividad_id, 
                    actividad_nombre, 
                    tribu_equipo, 
                    fecha_actual
                ))

            sql = """
                INSERT INTO resultados_sorteo 
                (idEstudiante, idActividad, nombreActividad, tribu_equipo, fecha_sorteo) 
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.executemany(sql, valores)
            exitosos += len(valores)

        conexion.commit()
        print(f"\n ¡ÉXITO! Se guardaron {exitosos} registros de participantes en la tabla 'resultados_sorteo'.")

    except Exception as e:
        conexion.rollback()
        print(f"Error al guardar resultados en la BD: {e}")
    finally:
        cursor.close()
        conexion.close()

def mostrar_menu():
    """Muestra el menú de opciones."""
    print("\n" + "=" * 40)
    print("      MENÚ SORTEO INTERTRIBUS")
    print("=" * 40)
    print("1 - Mostrar inscriptos")
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



