from fastapi import APIRouter, HTTPException
from models.consulta_productos import obtener_productos



router = APIRouter(prefix="/consulta_productos", tags=["Consulta de Productos"])

@router.get("/")
def listar_productos(nombre: str = "", categoria: str = "", estado: str = ""):
    try:
        productos = obtener_productos(nombre, categoria, estado)
        return productos
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener productos: {str(e)}")
