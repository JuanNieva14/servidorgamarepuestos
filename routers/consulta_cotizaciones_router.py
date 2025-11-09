from fastapi import APIRouter, HTTPException
from models.consulta_cotizaciones import listar_cotizaciones

router = APIRouter()

@router.get("/consulta_cotizaciones")
def get_cotizaciones():
    try:
        return listar_cotizaciones()
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail="Error al obtener cotizaciones")
