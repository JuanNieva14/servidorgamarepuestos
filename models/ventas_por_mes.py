from datetime import datetime
from decimal import Decimal
from fastapi import HTTPException
from database import get_conn


def obtener_ventas_por_mes():
    conn = get_conn()
    cursor = None
    try:
        query = """
            SELECT 
                DATE_FORMAT(MIN(f.fecha_factura), '%Y-%m') AS mes,
                SUM(f.subtotal) AS subtotal_total,
                SUM(f.impuesto) AS impuesto_total,
                SUM(f.descuento) AS descuento_total,
                SUM(f.total) AS total_general,
                COUNT(f.id_factura) AS numero_facturas
            FROM facturas f
            INNER JOIN estados e ON f.id_estado = e.id_estado
            WHERE e.nombre_estado NOT IN ('Anulada', 'Cancelada')
            GROUP BY YEAR(f.fecha_factura), MONTH(f.fecha_factura)
            ORDER BY YEAR(f.fecha_factura) DESC, MONTH(f.fecha_factura) DESC;
        """

        cursor = conn.cursor(dictionary=True)
        cursor.execute(query)
        resultados = cursor.fetchall()

        # 🗓️ Mapeo manual de meses en español
        meses_es = {
            "January": "Enero", "February": "Febrero", "March": "Marzo",
            "April": "Abril", "May": "Mayo", "June": "Junio",
            "July": "Julio", "August": "Agosto", "September": "Septiembre",
            "October": "Octubre", "November": "Noviembre", "December": "Diciembre"
        }

        datos_convertidos = []
        for fila in resultados:
            fila_limpia = {}
            for clave, valor in fila.items():
                if isinstance(valor, Decimal):
                    fila_limpia[clave] = float(valor)
                else:
                    fila_limpia[clave] = valor

            # Convertir “YYYY-MM” → “Mes YYYY” en español
            try:
                fecha = datetime.strptime(fila_limpia["mes"], "%Y-%m")
                mes_en = fecha.strftime("%B")
                anio = fecha.strftime("%Y")
                fila_limpia["mes"] = f"{meses_es[mes_en]} {anio}"
            except:
                pass

            datos_convertidos.append(fila_limpia)

        return datos_convertidos

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener ventas por mes: {e}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
