# ============================================================================
# Script de Python para interactuar con la BBDD 'tecno_city_normalizado'
# ============================================================================

import mysql.connector
from mysql.connector import Error

# --- Módulo de Conexión ---
def crear_conexion():
    """Crea y devuelve un objeto de conexión a la base de datos."""
    try:
        conexion = mysql.connector.connect(
            host='localhost',
            user='root',
            password='', # <-- REEMPLAZAR
            database='tecno_city_normalizado'
        )
        if conexion.is_connected():            
            print("Conexión a 'tecno_city_normalizado' exitosa.")
            return conexion
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

# --- Bloque 1: Modificciòn del Estado del Negocio (DML) ---

def ejercicio_1_insertar_productos():
    print("\n--- Ejecutando Ejercicio 1: INSERT ---")
    conexion = crear_conexion()
    if conexion is None: return

    try:
        cursor = conexion.cursor()
        nuevos_productos = [
            ('Tablet Genérica 10 pulgadas', 1, 180.50),
            ('Soporte para Laptop', 3, 45.00)
        ]
        consulta_sql = "INSERT INTO PRODUCTOS (nombre_producto, id_categoria_fk, precio) VALUES (%s, %s, %s)"
        
        cursor.executemany(consulta_sql, nuevos_productos)
        conexion.commit() # Guarda los cambios.
        
        print(f"{cursor.rowcount} productos han sido insertados exitosamente.")

    except Error as e:
        print(f"Error al insertar productos: {e}")
    finally:
        cursor.close()
        conexion.close()

def ejercicio_2_actualizar_precios():
    print("\n--- Ejecutando Ejercicio 2: UPDATE ---")
    conexion = crear_conexion()
    if conexion is None: return

    try:
        cursor = conexion.cursor()
        consulta_sql = """
        UPDATE PRODUCTOS
        SET precio = precio * 1.10
        WHERE id_categoria_fk = 2;
        """
        cursor.execute(consulta_sql)
        conexion.commit()
        print(f"{cursor.rowcount} productos de la categoría 'Laptops' han sido actualizados.")
    except Error as e:
        print(f"Error al actualizar precios: {e}")
    finally:
        cursor.close()
        conexion.close()

def ejercicio_3_eliminar_producto():
    print("\n--- Ejecutando Ejercicio 3: DELETE ---")
    conexion = crear_conexion()
    if conexion is None: return
    
    try:
        cursor = conexion.cursor()
        consulta_sql = "DELETE FROM PRODUCTOS WHERE id_producto = 7;"
        cursor.execute(consulta_sql)
        conexion.commit()
        
        if cursor.rowcount > 0:
            print("El producto 'Mouse Ergonómico' ha sido eliminado.")
        else:
            print("El producto 'Mouse Ergonómico' no fue encontrado o ya había sido eliminado.")
    except Error as e:
        print(f"Error al eliminar el producto: {e}")
    finally:
        cursor.close()
        conexion.close()

# --- Bloque 2: Análisis y Reportes ---

def ejecutar_consulta_e_imprimir(titulo, consulta_sql, encabezados):
    print(f"\n--- Ejecutando {titulo} ---")
    conexion = crear_conexion()
    if conexion is None: return

    try:
        cursor = conexion.cursor()
        cursor.execute(consulta_sql)
        resultados = cursor.fetchall()

        if resultados:
            print(" | ".join(encabezados))
            print("-" * 80)
            for fila in resultados:
                # Formatear cada celda para alinearla
                print(" | ".join(str(item).ljust(20) for item in fila))
        else:
            print("La consulta no devolvió resultados.")

    except Error as e:
        print(f"Error en la consulta: {e}")
    finally:
        cursor.close()
        conexion.close()

# --- Funciones para cada ejercicio de consulta ---

def ejercicio_4_inventario_por_categoria():
    sql = """
    SELECT c.nombre_categoria, COUNT(p.id_producto), ROUND(AVG(p.precio), 2), MAX(p.precio)
    FROM PRODUCTOS AS p JOIN CATEGORIAS AS c ON p.id_categoria_fk = c.id_categoria
    GROUP BY c.nombre_categoria ORDER BY c.nombre_categoria;
    """
    encabezados = ["Categoría", "Cant. Productos", "Precio Promedio", "Precio Máximo"]
    ejecutar_consulta_e_imprimir("Ejercicio 4: Inventario por Categoría", sql, encabezados)

def ejercicio_5_rendimiento_vendedores():
    sql = """
    SELECT CONCAT(v.nombre, ' ', v.apellido), SUM(df.cantidad * df.precio_unitario_hist)
    FROM VENDEDORES AS v
    JOIN FACTURAS AS f ON v.id_vendedor = f.id_vendedor_fk
    JOIN DETALLES_FACTURA AS df ON f.id_factura = df.id_factura_fk
    GROUP BY v.id_vendedor ORDER BY 2 DESC;
    """
    encabezados = ["Vendedor", "Monto Total Facturado"]
    ejecutar_consulta_e_imprimir("Ejercicio 5: Rendimiento de Vendedores", sql, encabezados)
    
def ejercicio_6_sucursales_bajo_volumen():
    sql = """
    SELECT s.nombre_sucursal, COUNT(f.id_factura)
    FROM SUCURSALES AS s JOIN FACTURAS AS f ON s.id_sucursal = f.id_sucursal_fk
    GROUP BY s.id_sucursal HAVING COUNT(f.id_factura) < 3 ORDER BY 2 ASC;
    """
    encabezados = ["Sucursal", "Cantidad de Facturas"]
    ejecutar_consulta_e_imprimir("Ejercicio 6: Sucursales con Bajo Volumen", sql, encabezados)
    
def ejercicio_7_categorias_rentables():
    sql = """
    SELECT c.nombre_categoria, SUM(df.cantidad * df.precio_unitario_hist) AS Ingreso
    FROM CATEGORIAS AS c
    JOIN PRODUCTOS AS p ON c.id_categoria = p.id_categoria_fk
    JOIN DETALLES_FACTURA AS df ON p.id_producto = df.id_producto_fk
    GROUP BY c.nombre_categoria HAVING Ingreso > 2000 ORDER BY Ingreso DESC;
    """
    encabezados = ["Categoría", "Ingreso Total"]
    ejecutar_consulta_e_imprimir("Ejercicio 7: Categorías más Rentables", sql, encabezados)

# --- Bloque 3: Consultas Detalladas y de Auditoría ---

def ejercicio_8_detalle_vendedor():
    sql = """
    SELECT f.id_factura, f.fecha_factura, p.nombre_producto, df.cantidad,
           df.precio_unitario_hist, (df.cantidad * df.precio_unitario_hist) AS Subtotal
    FROM VENDEDORES AS v
    JOIN FACTURAS AS f ON v.id_vendedor = f.id_vendedor_fk
    JOIN DETALLES_FACTURA AS df ON f.id_factura = df.id_factura_fk
    JOIN PRODUCTOS AS p ON df.id_producto_fk = p.id_producto
    WHERE v.nombre = 'Carlos' AND v.apellido = 'Rivas'
    ORDER BY f.fecha_factura, f.id_factura;
    """
    encabezados = ["ID Factura", "Fecha", "Producto", "Cantidad", "Precio Unit.", "Subtotal"]
    ejecutar_consulta_e_imprimir("Ejercicio 8: Detalle de Ventas de Carlos Rivas", sql, encabezados)

def ejercicio_9_productos_no_vendidos():
    sql = """
    SELECT p.nombre_producto, p.precio
    FROM PRODUCTOS AS p
    LEFT JOIN DETALLES_FACTURA AS df ON p.id_producto = df.id_producto_fk
    WHERE df.id_detalle IS NULL ORDER BY p.nombre_producto;
    """
    encabezados = ["Producto no vendido", "Precio de Lista"]
    ejecutar_consulta_e_imprimir("Ejercicio 9: Productos sin Ventas", sql, encabezados)

def ejercicio_10_jerarquia_vendedores():
    sql = """
    SELECT empleado.nombre, empleado.apellido, 
           COALESCE(CONCAT(supervisor.nombre, ' ', supervisor.apellido), 'Sin Supervisor')
    FROM VENDEDORES AS empleado
    LEFT JOIN VENDEDORES AS supervisor ON empleado.id_supervisor_fk = supervisor.id_vendedor
    ORDER BY empleado.apellido, empleado.nombre;
    """
    encabezados = ["Empleado Nombre", "Empleado Apellido", "Supervisor"]
    ejecutar_consulta_e_imprimir("Ejercicio 10: Jerarquía de Vendedores", sql, encabezados)


# --- Flujo Principal de Ejecución ---
if __name__ == '__main__':
    # Bloque 1: Modificaciones
    #ejercicio_1_insertar_productos()
    #ejercicio_2_actualizar_precios()
    #ejercicio_3_eliminar_producto()

    # Bloque 2 y 3: Consultas sobre los datos ya modificados
    ejercicio_4_inventario_por_categoria()
    ejercicio_5_rendimiento_vendedores()
    ejercicio_6_sucursales_bajo_volumen()
    ejercicio_7_categorias_rentables()
    ejercicio_8_detalle_vendedor()
    ejercicio_9_productos_no_vendidos()
    ejercicio_10_jerarquia_vendedores()