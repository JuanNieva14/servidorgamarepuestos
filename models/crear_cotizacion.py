from pydantic import BaseModel
from datetime import datetime
from database import get_conn



# Modelo de datos recibido desde el frontend
class Cotizacion(BaseModel):
    id_cliente: int
    id_producto: int
    cantidad: int
    fecha_cotizacion: datetime
