from database import conectar_bd

if __name__ == '__main__':
    conexion = conectar_bd()

    if conexion:
        print("Conexion exitosa.")
        conexion.close()
    else:
        print("Error al establecer una conexión.")