# models/inventario.py
from database import get_conn

def obtener_inventario():
    try:
        conn = get_conn()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                p.codigo_producto AS Codigo,
                p.nombre_producto AS Producto,
                c.nombre_categoria AS Categoria,
                p.precio_venta AS Precio_Venta,
                i.stock_actual AS Stock_Actual,
                i.stock_minimo AS Stock_Minimo,
                i.fecha_actualizacion AS Fecha_Actualizacion
            FROM inventarios i
            INNER JOIN productos p ON i.id_producto = p.id_producto
            INNER JOIN categorias c ON p.id_categoria = c.id_categoria
            ORDER BY p.nombre_producto ASC;
        """)
        data = cursor.fetchall()
        conn.close()
        return data
    except Exception as e:
        print("Error al obtener inventario:", e)
        raise Exception("Error al obtener inventario")


def actualizar_stock(codigo_producto: str, nuevo_stock: int):
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE inventarios i
            INNER JOIN productos p ON i.id_producto = p.id_producto
            SET i.stock_actual = %s, i.fecha_actualizacion = NOW()
            WHERE p.codigo_producto = %s;
        """, (nuevo_stock, codigo_producto))
        conn.commit()
        conn.close()

        if cursor.rowcount == 0:
            return {"ok": False, "mensaje": "Código de producto no encontrado"}
        return {"ok": True, "mensaje": "Stock actualizado correctamente"}
    except Exception as e:
        print("Error al actualizar stock:", e)
        return {"ok": False, "mensaje": f"Error: {e}"}
