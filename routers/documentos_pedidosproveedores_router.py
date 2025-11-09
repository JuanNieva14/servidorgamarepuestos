# routers/documentos_pedidosproveedores_router.py
from fastapi import APIRouter, HTTPException
from models.documentos_pedidosproveedores import obtener_pedidos_proveedores, obtener_detalle_pedido

router = APIRouter()

@router.get("/pedidosproveedores")
def get_pedidos_proveedores():
    try:
        data = obtener_pedidos_proveedores()
        return data
    except Exception as e:
        print("❌ Error en get_pedidos_proveedores:", e)
        raise HTTPException(status_code=500, detail=f"Error al obtener pedidos de proveedores: {e}")


@router.get("/pedidosproveedores/{id_pedido}")
def get_detalle_pedido(id_pedido: int):
    try:
        data = obtener_detalle_pedido(id_pedido)
        if not data:
            raise HTTPException(status_code=404, detail="Pedido no encontrado")
        return data
    except Exception as e:
        print("❌ Error en get_detalle_pedido:", e)
        raise HTTPException(status_code=500, detail=f"Error al obtener detalle de pedido: {e}")
