from fastapi import APIRouter, HTTPException
from models.ventasproductos import insertar_venta

router = APIRouter(prefix="/ventasproductos", tags=["Ventas de Productos"])

@router.post("/")
def registrar_venta(data: dict):
    """
    Registra una venta de productos (factura + detalle).
    """
    try:
        id_cliente = data.get("id_cliente")
        id_usuario = data.get("id_usuario", 1)
        id_forma_pago = data.get("id_forma_pago")
        productos = data.get("productos", [])

        if not id_cliente or not id_forma_pago or not productos:
            raise HTTPException(status_code=400, detail="Datos incompletos para registrar la venta")

        resultado = insertar_venta(id_cliente, id_usuario, id_forma_pago, productos)
        return resultado

    except Exception as e:
        print(f"❌ Error al registrar venta: {e}")
        raise HTTPException(status_code=500, detail=f"Error al registrar venta: {e}")
