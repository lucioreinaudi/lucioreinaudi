from database import conectar_bd

def main():
    conexion = conectar_bd()

    if conexion:
        print("Conexión exitosa.")
        conexion.close()
    else:
        print("Error al establecer la conexión.")

if __name__ == '__main__':
    main()
