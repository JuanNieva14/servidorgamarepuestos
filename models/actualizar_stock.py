from database import get_conn

from datetime import datetime


# 📦 Obtener producto por nombre
def buscar_producto(nombre_producto: str):
    conn = get_conn()


    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT 
                i.id_inventario,
                p.id_producto,
                p.nombre_producto AS nombre,
                i.stock_actual,
                i.stock_minimo
            FROM inventarios i
            INNER JOIN productos p ON i.id_producto = p.id_producto
            WHERE p.nombre_producto LIKE %s
            ORDER BY p.nombre_producto ASC
        """, (f"%{nombre_producto}%",))
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

# 🔄 Actualizar stock
def actualizar_stock(id_producto: int, nuevo_stock: int):
    conn = get_conn()
    cursor = conn.cursor()
    try:
        fecha_actualizacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("""
            UPDATE inventarios
            SET stock_actual = %s,
                fecha_actualizacion = %s
            WHERE id_producto = %s
        """, (nuevo_stock, fecha_actualizacion, id_producto))

        conn.commit()
        return {"ok": True, "mensaje": "✅ Stock actualizado correctamente"}
    except Exception as e:
        conn.rollback()
        raise Exception(f"Error al actualizar stock: {e}")
    finally:
        cursor.close()
        conn.close()
