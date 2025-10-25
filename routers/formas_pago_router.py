from fastapi import APIRouter, HTTPException
from models import formas_pago
from models.formas_pago import FormaPago

router = APIRouter(prefix="/formas_pago", tags=["Formas de Pago"])

@router.get("/")
def listar_formas_pago():
    try:
        return formas_pago.obtener_todos()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/")
def crear_forma_pago(forma: FormaPago):
    try:
        formas_pago.crear_forma_pago(forma)
        return {"mensaje": "✅ Forma de pago registrada correctamente."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{id_forma_pago}")
def actualizar_forma_pago(id_forma_pago: int, forma: FormaPago):
    try:
        if not formas_pago.obtener_por_id(id_forma_pago):
            raise HTTPException(status_code=404, detail="Forma de pago no encontrada.")
        formas_pago.actualizar_forma_pago(id_forma_pago, forma)
        return {"mensaje": "✅ Forma de pago actualizada correctamente."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{id_forma_pago}")
def eliminar_forma_pago(id_forma_pago: int):
    try:
        if not formas_pago.obtener_por_id(id_forma_pago):
            raise HTTPException(status_code=404, detail="Forma de pago no encontrada.")
        formas_pago.eliminar_forma_pago(id_forma_pago)
        return {"mensaje": "🗑️ Forma de pago eliminada correctamente."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
