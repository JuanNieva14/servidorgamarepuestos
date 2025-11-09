# routers/login_router.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from models.login import verificar_credenciales

router = APIRouter(prefix="/login", tags=["Login"])

class LoginRequest(BaseModel):
    usuario: str
    contrasena: str

@router.post("/")
def login(request: LoginRequest):
    resultado = verificar_credenciales(request.usuario, request.contrasena)

    if resultado:
        print("✅ Usuario autenticado:", resultado["usuario"])

        return JSONResponse(
            content={
                "ok": True,
                "usuario": {
                    "id_usuario": resultado.get("id_usuario"),
                    "usuario": resultado.get("usuario"),
                    "nombre": resultado.get("nombre"),
                    "apellido": resultado.get("apellido"),
                    "documento": resultado.get("documento"),
                    "correo": resultado.get("correo"),
                    "rol": resultado.get("id_rol"),
                }
            },
            status_code=200
        )

    raise HTTPException(status_code=401, detail="Credenciales incorrectas")
