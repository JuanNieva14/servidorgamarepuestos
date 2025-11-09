from database import get_conn
from fastapi import HTTPException

def obtener_facturacion_periodo(busqueda: str = "", mes: str = "Todos"):
    try:
        conn = get_conn()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT 
                CONCAT(p.nombre, ' ', p.apellido) AS cliente,
                ANY_VALUE(MONTHNAME(f.fecha_factura)) AS mes,
                COUNT(f.id_factura) AS facturas,
                SUM(f.total) AS total
            FROM facturas f
            INNER JOIN clientes c ON f.id_cliente = c.id_cliente
            INNER JOIN personas p ON c.id_persona = p.id_persona
            WHERE 1=1
        """

        params = []

        # 🔍 Filtro por nombre o apellido del cliente
        if busqueda:
            query += " AND (p.nombre LIKE %s OR p.apellido LIKE %s)"
            params.extend([f"%{busqueda}%", f"%{busqueda}%"])

        # 📅 Filtro por mes (acepta español)
        if mes != "Todos":
            meses_traducidos = {
                "Enero": "January", "Febrero": "February", "Marzo": "March",
                "Abril": "April", "Mayo": "May", "Junio": "June",
                "Julio": "July", "Agosto": "August", "Septiembre": "September",
                "Octubre": "October", "Noviembre": "November", "Diciembre": "December"
            }
            mes_ingles = meses_traducidos.get(mes, mes)
            query += " AND MONTHNAME(f.fecha_factura) = %s"
            params.append(mes_ingles)

        # ✅ Agrupación y orden 100 % compatibles con ONLY_FULL_GROUP_BY
        query += """
            GROUP BY cliente, MONTH(f.fecha_factura)
            ORDER BY ANY_VALUE(YEAR(f.fecha_factura)) DESC, ANY_VALUE(MONTH(f.fecha_factura)) DESC;
        """

        cursor.execute(query, params)
        resultados = cursor.fetchall()

        # 🧮 Convertir Decimals a float
        for r in resultados:
            r["total"] = float(r["total"]) if r["total"] is not None else 0.0

        return {"success": True, "data": resultados}

    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Error al obtener facturación: {err}")

    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()
