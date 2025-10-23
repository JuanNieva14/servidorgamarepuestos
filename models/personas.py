from pydantic import BaseModel
from typing import Optional

class Persona(BaseModel):
    id_persona: Optional[int] = None
    numero_documento: str
    nombre: str
    apellido: str
    correo: str
    direccion: str
    fecha_creacion: Optional[str] = None
    estado: Optional[str] = "Activo"
