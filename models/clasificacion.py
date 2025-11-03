from pydantic import BaseModel

class Clasificacion(BaseModel):
    nombre_clasificacion: str
    tipo: str
    activo: int | None = 1
