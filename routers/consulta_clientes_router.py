from fastapi import APIRouter, HTTPException
from models.consulta_clientes import obtener_clientes

router = APIRouter(prefix="/consulta_clientes", tags=["Consulta de Clientes"])

@router.get("/")
def listar_clientes(busqueda: str = ""):
    try:
        return obtener_clientes(busqueda)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener clientes: {str(e)}")
