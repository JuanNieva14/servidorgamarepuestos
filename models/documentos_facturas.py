# models/documentos_facturas.py
from database import get_conn

def obtener_facturas():
    """
    Retorna la lista general de facturas para la vista principal.
    """
    conn = get_conn()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT
            f.id_factura,
            f.numero_factura,
            DATE_FORMAT(f.fecha_factura, '%Y-%m-%d') AS fecha_factura,
            CONCAT(pc.nombre, ' ', pc.apellido) AS cliente,
            pc.numero_documento AS documento_cliente,
            e.nombre_estado AS estado
        FROM facturas f
        INNER JOIN clientes c ON f.id_cliente = c.id_cliente
        INNER JOIN personas pc ON c.id_persona = pc.id_persona
        INNER JOIN estados e ON f.id_estado = e.id_estado
        ORDER BY f.id_factura DESC;
    """)
    data = cursor.fetchall()
    conn.close()
    return data


def obtener_detalle_factura(id_factura: int):
    """
    Retorna el detalle completo de una factura específica (para imprimir).
    """
    conn = get_conn()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT
                f.numero_factura AS factura,
                CONCAT(pc.nombre, ' ', pc.apellido) AS cliente,
                pc.numero_documento AS documento,
                pc.correo AS correo_cliente,
                fp.nombre_forma AS forma_pago,
                e.nombre_estado AS estado,
                CONCAT(pv.nombre, ' ', pv.apellido) AS vendedor,
                u.usuario AS usuario_vendedor,
                p.nombre_producto AS producto,
                df.cantidad AS cantidad,
                FORMAT(df.precio_unitario, 0, 'es_CO') AS precio_unitario,
                FORMAT(df.subtotal, 0, 'es_CO') AS subtotal,
                FORMAT(f.total, 0, 'es_CO') AS total_factura,
                DATE_FORMAT(f.fecha_factura, '%Y-%m-%d') AS fecha
            FROM facturas f
            INNER JOIN detalle_facturas df ON f.id_factura = df.id_factura
            INNER JOIN productos p ON df.id_producto = p.id_producto
            INNER JOIN clientes c ON f.id_cliente = c.id_cliente
            INNER JOIN personas pc ON c.id_persona = pc.id_persona
            INNER JOIN usuarios u ON f.id_usuario = u.id_usuario
            INNER JOIN personas pv ON u.id_persona = pv.id_persona
            INNER JOIN formas_pago fp ON f.id_forma_pago = fp.id_forma_pago
            INNER JOIN estados e ON f.id_estado = e.id_estado
            WHERE f.id_factura = %s;
        """, (id_factura,))
        data = cursor.fetchall()
        conn.close()
        return data
    except Exception as e:
        print("❌ Error en obtener_detalle_factura:", e)
        conn.close()
        return []
