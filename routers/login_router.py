# routers/login_router.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from models.login import verificar_credenciales


router = APIRouter()

class LoginRequest(BaseModel):
    usuario: str
    contrasena: str

@router.post("/login")
def login(request: LoginRequest):
    resultado = verificar_credenciales(request.usuario, request.contrasena)
    if resultado:
        return {
            "mensaje": "Acceso concedido",
            "usuario": resultado["usuario"],
            "perfil": resultado
        }
    else:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
