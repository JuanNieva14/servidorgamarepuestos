from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from models.consulta_proveedores import (
    obtener_proveedores,
    agregar_proveedor,
    actualizar_proveedor,
    eliminar_proveedor,
)

router = APIRouter()

class Proveedor(BaseModel):
    nit: str
    nombre: str
    apellido: str
    tipo_documento: str
    numero_documento: str
    correo: str
    direccion: str
    id_ciudad: int

@router.get("/consulta_proveedores")
def listar_proveedores():
    try:
        return obtener_proveedores()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener proveedores: {e}")


@router.post("/consulta_proveedores")
def crear_proveedor(proveedor: Proveedor):
    try:
        return agregar_proveedor(
            proveedor.nit,
            proveedor.nombre,
            proveedor.apellido,
            proveedor.tipo_documento,
            proveedor.numero_documento,
            proveedor.correo,
            proveedor.direccion,
            proveedor.id_ciudad
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear proveedor: {e}")


@router.put("/consulta_proveedores/{id_proveedor}")
def editar_proveedor(id_proveedor: int, proveedor: Proveedor):
    try:
        return actualizar_proveedor(
            id_proveedor,
            proveedor.nit,
            proveedor.nombre,
            proveedor.apellido,
            proveedor.tipo_documento,
            proveedor.numero_documento,
            proveedor.correo,
            proveedor.direccion,
            proveedor.id_ciudad
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar proveedor: {e}")


@router.delete("/consulta_proveedores/{id_proveedor}")
def borrar_proveedor(id_proveedor: int):
    try:
        return eliminar_proveedor(id_proveedor)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar proveedor: {e}")
