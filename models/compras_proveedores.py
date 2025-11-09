from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import JSONResponse
from database import get_conn

router = APIRouter()

@router.get("/compras_proveedores")
def obtener_compras_proveedores(
    busqueda: str = Query("", description="Buscar por proveedor"),
    mes: str = Query("Todos", description="Filtrar por mes")
):
    conn = get_conn()
    cursor = None
    try:
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT 
                pr.id_proveedor,
                CONCAT(pe.nombre, ' ', pe.apellido) AS proveedor,
                MONTHNAME(pp.fecha_pedido) AS mes,
                COUNT(pp.id_pedido) AS facturas
            FROM pedidos_proveedores pp
            INNER JOIN proveedores pr ON pp.id_proveedor = pr.id_proveedor
            INNER JOIN personas pe ON pr.id_persona = pe.id_persona
            WHERE 
                (%s = '' OR pe.nombre LIKE %s OR pe.apellido LIKE %s)
                AND (%s = 'Todos' OR MONTHNAME(pp.fecha_pedido) = %s)
            GROUP BY pr.id_proveedor, mes
            ORDER BY mes ASC, proveedor ASC;
        """


        valores = (busqueda, f"%{busqueda}%", f"%{busqueda}%", mes, mes)
        cursor.execute(query, valores)
        resultados = cursor.fetchall()


        # 🧮 Agregamos un total simulado por ahora (solo para visualizar en el frontend)
        for r in resultados:
            r["total"] = 500000 * r["facturas"]  # ejemplo: 500.000 COP por factura

        return {"success": True, "data": resultados}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener compras: {e}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
