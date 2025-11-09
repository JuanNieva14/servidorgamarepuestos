from fastapi import APIRouter, Body, Path
from models.gestion_pedidos_proveedores import (
    listar_pedidos_proveedores,
    crear_pedido_proveedor,
    actualizar_pedido_proveedor,
    eliminar_pedido_proveedor,
    listar_proveedores_select,
    listar_vendedores_select,
    listar_estados_select,
)

router = APIRouter(prefix="/pedidos_proveedores", tags=["Gestión Pedidos Proveedores"])

@router.get("/")
def get_pedidos():
    return listar_pedidos_proveedores()

@router.get("/proveedores_select")
def get_proveedores_select():
    return listar_proveedores_select()

@router.get("/vendedores_select")
def get_vendedores_select():
    return listar_vendedores_select()

@router.get("/estados_select")
def get_estados_select():
    return listar_estados_select()

@router.post("/")
def post_pedido(data: dict = Body(...)):
    return crear_pedido_proveedor(data)

@router.put("/{id_pedido}")
def put_pedido(id_pedido: int = Path(...), data: dict = Body(...)):
    return actualizar_pedido_proveedor(id_pedido, data)

@router.delete("/{id_pedido}")
def delete_pedido(id_pedido: int = Path(...)):
    return eliminar_pedido_proveedor(id_pedido)
