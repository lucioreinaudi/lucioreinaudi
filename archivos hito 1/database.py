import pymysql

DB_CONFIG = {
    'user': 'root',
    'password': '',
    'host': '127.0.0.1',
    'database': 'intertribu',
    'port': 3307,
    'charset': 'utf8mb4',
    'connect_timeout': 5
}

def conectar_bd():
    try:
        conexion = pymysql.connect(**DB_CONFIG)
        print("Conexión exitosa a la base de datos.")
        return conexion
    except Exception as err:
        print(f"Error al conectar: {err}")
        return None


