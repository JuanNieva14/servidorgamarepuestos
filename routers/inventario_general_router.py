
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from models.inventario_general import obtener_inventario_general
from fastapi import Query

router = APIRouter(prefix="/inventario_general", tags=["📦 Inventario General"])

@router.get("/")
def listar_inventario(
    page: int = Query(1, ge=1, description="Número de página"),
    page_size: int = Query(10, ge=1, le=100, description="Tamaño de página (registros por página)")
):
    try:
        inventario = obtener_inventario_general(page, page_size)
        return JSONResponse(content=inventario)
    except Exception as e:
        return JSONResponse(status_code=500, content={"success": False, "error": str(e)})
