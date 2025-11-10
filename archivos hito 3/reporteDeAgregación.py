def tablaIinscripcionesVacia():
    """Verifica si la tabla de inscripciones tiene datos."""
    conexion = conectar_bd()
    if not conexion:
        return False
    cursor = conexion.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM inscripciones")
        cantidad = cursor.fetchone()[0]
        return cantidad == 0
    except Exception:
        return False
    finally:
        cursor.close()
        conexion.close()
