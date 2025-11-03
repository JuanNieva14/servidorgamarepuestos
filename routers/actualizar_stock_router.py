from fastapi import APIRouter, HTTPException
from models.actualizar_stock import buscar_producto, actualizar_stock

router = APIRouter(prefix="/stock", tags=["Actualizar Stock"])

# 🔍 Buscar producto por nombre
@router.get("/buscar/{nombre}")
def get_producto(nombre: str):
    try:
        productos = buscar_producto(nombre)
        if not productos:
            return {"ok": False, "mensaje": "No se encontraron productos"}
        return productos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 🔄 Actualizar stock
@router.put("/actualizar/{id_producto}/{nuevo_stock}")
def put_stock(id_producto: int, nuevo_stock: int):
    try:
        resultado = actualizar_stock(id_producto, nuevo_stock)
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
