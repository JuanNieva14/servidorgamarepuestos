from pydantic import BaseModel
from database import get_conn

  # Ajusta si tu conexión está en otro archivo

class ConsultaProducto(BaseModel):
    id_producto: int | None = None
    nombre: str | None = None
    categoria: str | None = None
    precio: float | None = None
    stock: int | None = None
    estado: str | None = None

def obtener_productos(nombre: str = "", categoria: str = "", estado: str = ""):
    conexion = get_conn()
    cursor = conexion.cursor(dictionary=True)
    query = """
        SELECT 
            p.id_producto,
            p.nombre_producto AS nombre,
            c.nombre_categoria AS categoria,
            p.precio_venta AS precio,
            i.stock_actual AS stock,
            e.nombre_estado AS estado
        FROM productos p
        INNER JOIN categorias c ON p.id_categoria = c.id_categoria
        INNER JOIN estados e ON p.id_estado = e.id_estado
        LEFT JOIN inventarios i ON p.id_producto = i.id_producto
        WHERE p.nombre_producto LIKE %s
    """
    filtros = [f"%{nombre}%"]

    if categoria:
        query += " AND c.nombre_categoria = %s"
        filtros.append(categoria)

    if estado:
        query += " AND e.nombre_estado = %s"
        filtros.append(estado)

    query += " ORDER BY p.nombre_producto ASC"
    cursor.execute(query, filtros)
    resultado = cursor.fetchall()
    cursor.close()
    conexion.close()
    return resultado
