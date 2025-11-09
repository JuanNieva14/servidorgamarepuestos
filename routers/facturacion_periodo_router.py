from fastapi import APIRouter, Query
from models.facturacion_periodo import obtener_facturacion_periodo

router = APIRouter()

@router.get("/facturacion_periodo")
def listar_facturacion_periodo(
    busqueda: str = Query("", description="Buscar por nombre o apellido del proveedor"),
    mes: str = Query("Todos", description="Filtrar por mes (en inglés: January, February, etc.)")
):
    return obtener_facturacion_periodo(busqueda, mes)
