from database import get_conn

def listar_cotizaciones():
    try:
        conn = get_conn()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT
                f.numero_factura AS numero_factura,
                CONCAT(pc.nombre, ' ', pc.apellido) AS cliente,
                FORMAT(f.total, 0, 'es_CO') AS total,
                DATE_FORMAT(f.fecha_factura, '%Y-%m-%d') AS fecha,
                e.nombre_estado AS estado
            FROM facturas f
            INNER JOIN clientes c ON f.id_cliente = c.id_cliente
            INNER JOIN personas pc ON c.id_persona = pc.id_persona
            INNER JOIN estados e ON f.id_estado = e.id_estado
            WHERE f.es_cotizacion = 1
            ORDER BY f.fecha_factura DESC
        """)
        datos = cursor.fetchall()
        conn.close()
        return datos
    except Exception as e:
        print("❌ Error listar_cotizaciones:", e)
        return []
