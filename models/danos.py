from pydantic import BaseModel
from datetime import datetime
from database import get_conn

# --- Modelo Pydantic ---
class Dano(BaseModel):
    id_producto: int
    cantidad: int
    motivo: str

class DanoDB(Dano):
    id_producto_danado: int
    fecha_registro: datetime
