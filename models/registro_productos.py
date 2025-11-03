# models/registro_productos.py
from database import get_conn
from datetime import datetime

def generar_codigo_producto(nombre_producto):
    """
    Genera un código tipo: Aceite 10W-40 Bajaj (Original OEM) -> P-A1W4BOO
    """
    partes = nombre_producto.upper().split()
    codigo = "P-"
    for p in partes:
        letras = ''.join([c for c in p if c.isalnum()])
        if letras:
            codigo += letras[0]
    return codigo[:10]


def obtener_categorias():
    try:
        conn = get_conn()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id_categoria, nombre_categoria FROM categorias ORDER BY nombre_categoria ASC")
        data = cursor.fetchall()
        conn.close()
        return data
    except Exception as e:
        raise Exception(f"Error al obtener categorías: {e}")


def obtener_clasificaciones():
    try:
        conn = get_conn()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id_clasificacion, nombre_clasificacion FROM clasificaciones ORDER BY nombre_clasificacion ASC")
        data = cursor.fetchall()
        conn.close()
        return data
    except Exception as e:
        raise Exception(f"Error al obtener clasificaciones: {e}")


def registrar_producto(datos):
    try:
        conn = get_conn()
        cursor = conn.cursor()

        codigo = generar_codigo_producto(datos["nombre_producto"])

        compra = float(datos["precio_compra"])
        venta = float(datos["precio_venta"])
        if compra <= 0:
            raise ValueError("El precio de compra debe ser mayor a 0")
        margen = round(((venta - compra) / compra) * 100, 2)

        cursor.execute("""
            INSERT INTO productos (
                codigo_producto, nombre_producto, descripcion, id_categoria,
                id_clasificacion, id_estado, precio_compra, precio_venta,
                activo, fecha_creacion, fecha_modificacion
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 1, NOW(), NOW())
        """, (
            codigo, datos["nombre_producto"], datos["descripcion"],
            datos["id_categoria"], datos["id_clasificacion"], datos["id_estado"],
            datos["precio_compra"], datos["precio_venta"]
        ))

        id_producto = cursor.lastrowid

        cursor.execute("""
            INSERT INTO inventarios (id_producto, stock_actual, stock_minimo, fecha_actualizacion)
            VALUES (%s, %s, %s, NOW())
        """, (
            id_producto, datos["stock_actual"], datos["stock_minimo"]
        ))

        conn.commit()
        conn.close()

        return {
            "ok": True,
            "mensaje": "Producto registrado correctamente",
            "codigo": codigo,
            "margen": f"{margen}%"
        }
    except Exception as e:
        print("Error al registrar producto:", e)
        return {"ok": False, "mensaje": str(e)}
