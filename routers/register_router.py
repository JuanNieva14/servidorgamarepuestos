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
    direccion: str
    contrasena: str
    confirmar: str

@router.post("/register_persona_usuario")
def register_persona_usuario(request: RegisterPersonaUsuario):
    if request.contrasena != request.confirmar:
        raise HTTPException(status_code=400, detail="Las contraseñas no coinciden")

    conn = get_conn()
    cursor = conn.cursor(dictionary=True)

    try:
        # 🔍 1️⃣ Verificar si el documento ya existe
        cursor.execute(
            "SELECT id_persona FROM personas WHERE numero_documento = %s",
            (request.numero_documento,)
        )
        persona_existente = cursor.fetchone()

        if persona_existente:
            raise HTTPException(
                status_code=400,
                detail="Ya existe una persona con este número de documento."
            )

        # 📧 2️⃣ Generar correo automático
        ultimos_tres = request.numero_documento[-3:]  # Últimos tres dígitos
        correo_auto = f"{request.nombre.lower()}.{request.apellido.lower()}{ultimos_tres}@gama.com"

        # 🧾 3️⃣ Insertar nueva persona
        cursor.execute(
            """
            INSERT INTO personas (tipo_documento, numero_documento, nombre, apellido, correo, direccion)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            ("CC", request.numero_documento, request.nombre, request.apellido, correo_auto, request.direccion)
        )
        conn.commit()
        id_persona = cursor.lastrowid

        # 👤 4️⃣ Generar usuario: primera letra del nombre + apellido
        usuario_generado = (request.nombre[0] + request.apellido + ultimos_tres).lower()

        # 🔒 5️⃣ Encriptar contraseña
        hashed = bcrypt.hashpw(request.contrasena.encode("utf-8"), bcrypt.gensalt())

        # 🧩 6️⃣ Insertar usuario con rol=1 (por defecto)
        cursor.execute(
            """
            INSERT INTO usuarios (usuario, contrasena, id_persona, id_rol, activo)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (usuario_generado, hashed.decode("utf-8"), id_persona, 1, 1)
        )
        conn.commit()

        # ✅ 7️⃣ Respuesta con usuario y correo generado
        return {
            "ok": True,
            "mensaje": "Cuenta creada exitosamente",
            "usuario": usuario_generado,
            "correo": correo_auto,
            "id_persona": id_persona
        }

    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        print("❌ Error al registrar cuenta:", e)
        raise HTTPException(status_code=500, detail=f"Error al registrar cuenta: {e}")
    finally:
        cursor.close()
        conn.close()
