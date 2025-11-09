def mostrarInscripciones(conexion):
    """Muestra los inscritos detallados con formato de tabla."""
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
