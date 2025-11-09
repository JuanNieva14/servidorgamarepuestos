from fastapi import HTTPException
from database import get_conn
from decimal import Decimal
from fastapi import HTTPException
from decimal import Decimal

def obtener_inventario_general(page: int = 1, page_size: int = 10):
    conn = get_conn()
    cursor = None
    try:
        cursor = conn.cursor(dictionary=True)

        # Calcular desplazamiento (OFFSET)
        offset = (page - 1) * page_size

        # 🔹 Consulta principal con límite y desplazamiento
        query = f"""
            SELECT 
                p.codigo_producto AS codigo,
                p.nombre_producto AS producto,
                c.nombre_categoria AS categoria,
                cl.nombre_clasificacion AS clasificacion,
                e.nombre_estado AS estado,
                i.stock_actual,
                i.stock_minimo,
                p.precio_compra,
                p.precio_venta,
                ROUND(((p.precio_venta - p.precio_compra) / p.precio_compra) * 100, 2) AS margen,
                DATE_FORMAT(i.fecha_actualizacion, '%Y-%m-%d %H:%i:%s') AS fecha_actualizacion
            FROM inventarios i
            INNER JOIN productos p ON i.id_producto = p.id_producto
            LEFT JOIN categorias c ON p.id_categoria = c.id_categoria
            LEFT JOIN clasificaciones cl ON p.id_clasificacion = cl.id_clasificacion
            LEFT JOIN estados e ON p.id_estado = e.id_estado
            ORDER BY p.nombre_producto ASC
            LIMIT {page_size} OFFSET {offset};
        """
        cursor.execute(query)
        resultados = cursor.fetchall()

        # 🔹 Consulta para contar el total de registros (sin LIMIT)
        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM inventarios i
            INNER JOIN productos p ON i.id_producto = p.id_producto
        """)
        total = cursor.fetchone()["total"]

        # 🔹 Convertir Decimals a float para evitar error JSON
        datos_convertidos = []
        for fila in resultados:
            fila_limpia = {}
            for clave, valor in fila.items():
                if isinstance(valor, Decimal):
                    fila_limpia[clave] = float(valor)
                else:
                    fila_limpia[clave] = valor
            datos_convertidos.append(fila_limpia)

        # 🔹 Cálculo del número total de páginas
        total_pages = (total + page_size - 1) // page_size

        return {
            "success": True,
            "page": page,
            "page_size": page_size,
            "total_records": total,
            "total_pages": total_pages,
            "data": datos_convertidos
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener inventario: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
