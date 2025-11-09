# routers/consulta_cotizacion_router.py
from fastapi import APIRouter, HTTPException
from models.documentos_cotizacion import obtener_cotizaciones, obtener_detalle_cotizacion

router = APIRouter()

@router.get("/cotizaciones")
def get_cotizaciones():
    try:
        data = obtener_cotizaciones()
        return data
    except Exception as e:
        print("❌ Error en get_cotizaciones:", e)
        raise HTTPException(status_code=500, detail=f"Error al obtener cotizaciones: {e}")


@router.get("/cotizaciones/{id_cotizacion}")
def get_detalle_cotizacion(id_cotizacion: int):
    try:
        data = obtener_detalle_cotizacion(id_cotizacion)
        if not data:
            raise HTTPException(status_code=404, detail="Cotización no encontrada")
        return data
    except Exception as e:
        print("❌ Error en get_detalle_cotizacion:", e)
        raise HTTPException(status_code=500, detail=f"Error al obtener detalle de cotización: {e}")
