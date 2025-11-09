# models/documentos_pedidosproveedores.py
from database import get_conn

def obtener_pedidos_proveedores():
    """
    Retorna la lista general de pedidos a proveedores.
    """
    conn = get_conn()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT
            pp.id_pedido AS id_pedido,
            pp.numero_pedido AS numero_pedido,
            pr.nit AS nit_proveedor,
            CONCAT(perp.nombre, ' ', perp.apellido) AS proveedor,
            CONCAT(peru.nombre, ' ', peru.apellido) AS usuario,
            e.nombre_estado AS estado,
            DATE_FORMAT(pp.fecha_pedido, '%Y-%m-%d') AS fecha_pedido,
            DATE_FORMAT(pp.fecha_entrega_esperada, '%Y-%m-%d') AS fecha_entrega,
            FORMAT(pp.total, 0, 'es_CO') AS total,
            pp.observaciones AS observaciones,
            DATE_FORMAT(pp.fecha_registro, '%Y-%m-%d %H:%i:%s') AS fecha_registro
        FROM pedidos_proveedores pp
        INNER JOIN proveedores pr ON pp.id_proveedor = pr.id_proveedor
        INNER JOIN personas perp ON pr.id_persona = perp.id_persona
        INNER JOIN usuarios u ON pp.id_usuario = u.id_usuario
        INNER JOIN personas peru ON u.id_persona = peru.id_persona
        INNER JOIN estados e ON pp.id_estado = e.id_estado
        ORDER BY pp.fecha_pedido DESC;
    """)
    data = cursor.fetchall()
    conn.close()
    return data


def obtener_detalle_pedido(id_pedido: int):
    """
    Retorna el detalle completo de un pedido específico (para imprimir).
    """
    conn = get_conn()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT
                pp.numero_pedido AS pedido,
                pr.nit AS nit_proveedor,
                CONCAT(perp.nombre, ' ', perp.apellido) AS proveedor,
                CONCAT(peru.nombre, ' ', peru.apellido) AS usuario,
                e.nombre_estado AS estado,
                p.nombre_producto AS producto,
                dp.cantidad AS cantidad,
                FORMAT(dp.precio_unitario, 0, 'es_CO') AS precio_unitario,
                FORMAT(dp.subtotal, 0, 'es_CO') AS subtotal,
                FORMAT(pp.total, 0, 'es_CO') AS total_general,
                DATE_FORMAT(pp.fecha_pedido, '%Y-%m-%d') AS fecha_pedido,
                DATE_FORMAT(pp.fecha_entrega_esperada, '%Y-%m-%d') AS fecha_entrega,
                pp.observaciones AS observaciones
            FROM pedidos_proveedores pp
            INNER JOIN detalle_pedidos dp ON pp.id_pedido = dp.id_pedido
            INNER JOIN productos p ON dp.id_producto = p.id_producto
            INNER JOIN proveedores pr ON pp.id_proveedor = pr.id_proveedor
            INNER JOIN personas perp ON pr.id_persona = perp.id_persona
            INNER JOIN usuarios u ON pp.id_usuario = u.id_usuario
            INNER JOIN personas peru ON u.id_persona = peru.id_persona
            INNER JOIN estados e ON pp.id_estado = e.id_estado
            WHERE pp.id_pedido = %s;
        """, (id_pedido,))
        data = cursor.fetchall()
        conn.close()
        return data
    except Exception as e:
        print("❌ Error en obtener_detalle_pedido:", e)
        conn.close()
        return []
