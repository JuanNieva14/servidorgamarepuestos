from fastapi import APIRouter, HTTPException
from datetime import datetime
from models.crear_cotizacion import Cotizacion, get_conn

router = APIRouter(prefix="/cotizaciones", tags=["Cotizaciones"])

# 🔹 Obtener clientes
@router.get("/clientes")
def obtener_clientes():
    conexion = get_conn()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("""
        SELECT c.id_cliente, CONCAT(p.nombre, ' ', p.apellido) AS nombre
        FROM clientes c
        INNER JOIN personas p ON c.id_persona = p.id_persona
        ORDER BY p.nombre ASC
    """)
    clientes = cursor.fetchall()
    cursor.close()
    conexion.close()
    return clientes

# 🔹 Obtener productos disponibles
@router.get("/productos")
def obtener_productos():
    conexion = get_conn()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("""
        SELECT id_producto, nombre_producto, precio_venta
        FROM productos
        WHERE id_estado IN (3, 5, 6)
        ORDER BY nombre_producto ASC
    """)
    productos = cursor.fetchall()
    cursor.close()
    conexion.close()
    return productos

# 🔹 Crear cotización
@router.post("/crear")
def crear_cotizacion(data: Cotizacion):
    try:
        conexion = get_conn()
        cursor = conexion.cursor()

        # Generar número de cotización (C-AÑO-XXXX)
        year = datetime.now().year
        cursor.execute("SELECT COUNT(*) FROM cotizaciones WHERE YEAR(fecha_cotizacion) = %s", (year,))
        consecutivo = cursor.fetchone()[0] + 1
        numero_cotizacion = f"C-{year}-{str(consecutivo).zfill(4)}"

        # Obtener precio del producto
        cursor.execute("SELECT precio_venta FROM productos WHERE id_producto = %s", (data.id_producto,))
        precio = cursor.fetchone()
        if not precio:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        precio_unitario = float(precio[0])

        # Calcular totales
        subtotal = precio_unitario * data.cantidad
        impuesto = subtotal * 0.19  # IVA 19%
        total = subtotal + impuesto

        # Insertar cabecera de cotización
        cursor.execute("""
            INSERT INTO cotizaciones (numero_cotizacion, id_cliente, id_usuario, fecha_cotizacion, subtotal, impuesto, descuento, total, id_estado)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (numero_cotizacion, data.id_cliente, 1, datetime.now(), subtotal, impuesto, 0, total, 13))
        conexion.commit()

        id_cotizacion = cursor.lastrowid

        # Insertar detalle
        cursor.execute("""
            INSERT INTO detalle_cotizaciones (id_cotizacion, id_producto, cantidad, precio_unitario, subtotal)
            VALUES (%s, %s, %s, %s, %s)
        """, (id_cotizacion, data.id_producto, data.cantidad, precio_unitario, subtotal))
        conexion.commit()

        return {
            "mensaje": "✅ Cotización creada correctamente",
            "numero_cotizacion": numero_cotizacion,
            "subtotal": subtotal,
            "total": total,
            "id_cotizacion": id_cotizacion
        }

    except Exception as e:
        conexion.rollback()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

    finally:
        cursor.close()
        conexion.close()
