# models/register_model.py
import bcrypt
from database import get_conn

def registrar_usuario(
    usuario: str,
    contrasena: str,
    numero_documento: str,
):
    """
    Registra un nuevo usuario vinculado a una persona existente (por número de documento).
    Si la persona no existe, retorna error.
    """
    try:
        conn = get_conn()
        cursor = conn.cursor(dictionary=True)

        # Buscar persona por número de documento
        cursor.execute(
            "SELECT id_persona FROM personas WHERE numero_documento = %s", (numero_documento,)
        )
        persona = cursor.fetchone()

        if not persona:
            conn.close()
            return {"ok": False, "mensaje": "No existe una persona con ese número de documento."}

        id_persona = persona["id_persona"]

        # Verificar si el usuario ya existe
        cursor.execute("SELECT * FROM usuarios WHERE usuario = %s", (usuario,))
        if cursor.fetchone():
            conn.close()
            return {"ok": False, "mensaje": "El usuario ya existe."}

        # Encriptar contraseña
        hashed = bcrypt.hashpw(contrasena.encode("utf-8"), bcrypt.gensalt())

        # Insertar usuario vinculado
        cursor.execute(
            "INSERT INTO usuarios (usuario, contrasena, id_persona) VALUES (%s, %s, %s)",
            (usuario, hashed.decode("utf-8"), id_persona),
        )
        conn.commit()
        conn.close()

        return {"ok": True, "mensaje": "Usuario registrado correctamente y vinculado a persona."}

    except Exception as e:
        print("❌ Error en registrar_usuario:", e)
        return {"ok": False, "mensaje": f"Error: {e}"}
