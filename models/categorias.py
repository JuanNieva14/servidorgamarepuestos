from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from database import get_conn


class Categoria(BaseModel):
    id_categoria: Optional[int] = None
    nombre_categoria: str
    activo: Optional[int] = 1
    fecha_creacion: Optional[datetime] = None
    fecha_modificacion: Optional[datetime] = None
