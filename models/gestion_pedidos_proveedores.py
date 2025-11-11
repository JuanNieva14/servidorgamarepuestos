from pydantic import BaseModel
from typing import Optional
from datetime import date

class PedidoProveedor(BaseModel):
    id_pedido: Optional[int] = None
    numero_pedido: str
    id_proveedor: Optional[int] = None
    id_usuario: Optional[int] = None
    fecha_pedido: date
    fecha_entrega_esperada: Optional[date] = None
    id_estado: Optional[int] = None
    total: Optional[float] = None
    observaciones: Optional[str] = None

