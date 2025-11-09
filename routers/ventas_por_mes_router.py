# ventas_por_mes_router.py
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from models.ventas_por_mes import obtener_ventas_por_mes  # Asegúrate de que el archivo esté en el mismo directorio o ajusta el import

router = APIRouter(prefix="/ventas_por_mes", tags=["📊 Reporte de Ventas"])

@router.get("/")
def listar_ventas_por_mes():
    """
    Retorna las ventas agrupadas por mes y año con totales de subtotal, IVA, descuento y total general.
    """
    try:
        ventas = obtener_ventas_por_mes()
        return JSONResponse(content={"success": True, "data": ventas})
    except Exception as e:
        return JSONResponse(status_code=500, content={"success": False, "error": str(e)})
