# routers/documentos_facturas_router.py
from fastapi import APIRouter, HTTPException
from models.documentos_facturas import obtener_facturas, obtener_detalle_factura

router = APIRouter()

@router.get("/facturas")
def get_facturas():
    try:
        data = obtener_facturas()
        return data
    except Exception as e:
        print("❌ Error en get_facturas:", e)
        raise HTTPException(status_code=500, detail=f"Error al obtener facturas: {e}")


@router.get("/facturas/{id_factura}")
def get_detalle_factura(id_factura: int):
    try:
        data = obtener_detalle_factura(id_factura)
        if not data:
            raise HTTPException(status_code=404, detail="Factura no encontrada")
        return data
    except Exception as e:
        print("❌ Error en get_detalle_factura:", e)
        raise HTTPException(status_code=500, detail=f"Error al obtener detalle de factura: {e}")
