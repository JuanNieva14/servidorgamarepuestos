# routers/inventario_router.py
from fastapi import APIRouter, HTTPException
from models.inventario import obtener_inventario, actualizar_stock

router = APIRouter()

@router.get("/inventario")
def listar_inventario():
    try:
        return obtener_inventario()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/inventario/{codigo_producto}")
def modificar_stock(codigo_producto: str, nuevo_stock: int):
    resultado = actualizar_stock(codigo_producto, nuevo_stock)
    if resultado["ok"]:
        return resultado
    else:
        raise HTTPException(status_code=400, detail=resultado["mensaje"])
