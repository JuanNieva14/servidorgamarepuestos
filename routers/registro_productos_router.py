# routers/registro_productos_router.py
from fastapi import APIRouter, HTTPException
from models.registro_productos import (
    registrar_producto,
    obtener_categorias,
    obtener_clasificaciones,
)

router = APIRouter()

@router.get("/categorias")
def listar_categorias():
    try:
        return obtener_categorias()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/clasificaciones")
def listar_clasificaciones():
    try:
        return obtener_clasificaciones()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/registroproductos")
def registrar_nuevo_producto(datos: dict):
    resultado = registrar_producto(datos)
    if resultado["ok"]:
        return resultado
    else:
        raise HTTPException(status_code=400, detail=resultado["mensaje"])
