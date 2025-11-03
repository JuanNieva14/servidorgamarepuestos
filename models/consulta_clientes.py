from database import get_conn

def obtener_clientes(busqueda: str = ""):
    conexion = get_conn()
    cursor = conexion.cursor(dictionary=True)

    query = """
        SELECT 
            c.id_cliente,
            CONCAT(p.nombre, ' ', p.apellido) AS nombre,
            p.correo AS correo,
            p.direccion AS direccion,
            p.numero_documento AS documento,
            CASE 
                WHEN p.activo = 1 THEN 'Activo'
                ELSE 'Inactivo'
            END AS estado
        FROM clientes c
        INNER JOIN personas p ON c.id_persona = p.id_persona
        WHERE p.nombre LIKE %s OR p.apellido LIKE %s OR p.correo LIKE %s
        ORDER BY p.nombre ASC
    """

    filtro = [f"%{busqueda}%"] * 3
    cursor.execute(query, filtro)
    clientes = cursor.fetchall()

    cursor.close()
    conexion.close()
    return clientes
