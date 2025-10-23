from pydantic import BaseModel
from typing import Optional

class Producto(BaseModel):
    id_producto: Optional[int] = None
    nombre_producto: str
    precio_venta: float
    descripcion: Optional[str] = None
    id_categoria: Optional[int] = None
    id_estado: Optional[int] = None
