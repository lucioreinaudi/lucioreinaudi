from database import conectar_bd

conexion = conectar_bd()

if conexion:
    print("Conexion exitosa.")
    conexion.close()
else:
    print("Error al establecer una conexión.")

if __name__ == '__main__':
    main()
