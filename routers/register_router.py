# routers/register_persona_usuario_router.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import bcrypt
from database import get_conn

router = APIRouter()

class RegisterPersonaUsuario(BaseModel):
    nombre: str
    apellido: str
    numero_documento: str
    correo: str
    direccion: str
    contrasena: str
    confirmar: str

@router.post("/register_persona_usuario")
def register_persona_usuario(request: RegisterPersonaUsuario):
    if request.contrasena != request.confirmar:
        raise HTTPException(status_code=400, detail="Las contraseñas no coinciden")

    try:
        conn = get_conn()
        cursor = conn.cursor(dictionary=True)

        # Verificar si ya existe una persona
        cursor.execute("SELECT id_persona FROM personas WHERE numero_documento = %s", (request.numero_documento,))
        persona = cursor.fetchone()

        if not persona:
            # Insertar persona
            cursor.execute(
                """
                INSERT INTO personas (tipo_documento, numero_documento, nombre, apellido, correo, direccion)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                ("CC", request.numero_documento, request.nombre, request.apellido, request.correo, request.direccion)
            )
            conn.commit()
            id_persona = cursor.lastrowid
        else:
            id_persona = persona["id_persona"]

        # Verificar si ya existe usuario vinculado
        cursor.execute("SELECT * FROM usuarios WHERE id_persona = %s", (id_persona,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Esta persona ya tiene un usuario registrado")

        # Crear usuario
        hashed = bcrypt.hashpw(request.contrasena.encode("utf-8"), bcrypt.gensalt())
        cursor.execute(
            "INSERT INTO usuarios (usuario, contrasena, id_persona) VALUES (%s, %s, %s)",
            (request.nombre.lower() + request.apellido.lower(), hashed.decode("utf-8"), id_persona)
        )
        conn.commit()
        conn.close()

        return {"mensaje": "Cuenta creada exitosamente"}

    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail=f"Error al registrar cuenta: {e}")
