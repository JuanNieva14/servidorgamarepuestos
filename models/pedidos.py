from pydantic import BaseModel
from typing import Optional
from datetime import date

class Pedido(BaseModel):
    id_proveedor: int
    id_usuario: int
    id_estado: int
    fecha_entrega_esperada: Optional[date] = None
    total: float
    observaciones: Optional[str] = None
