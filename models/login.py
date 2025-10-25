# models/login.py
import bcrypt
from database import get_conn

def verificar_credenciales(usuario: str, contrasena: str):
    """
    Verifica si las credenciales coinciden con los datos almacenados en la base.
    Retorna el usuario (sin contraseña) si es correcto, o None si falla.
    """
    try:
        conn = get_conn()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE usuario = %s", (usuario,))
        data = cursor.fetchone()
        conn.close()

        if not data:
            print("⚠️ Usuario no encontrado en la base de datos.")
            return None

        # Corrige compatibilidad entre $2y$ (PHP) y $2b$ (Python)
        hash_guardado = data["contrasena"].encode("utf-8").replace(b"$2y$", b"$2b$")

        # Verificar contraseña
        if bcrypt.checkpw(contrasena.encode("utf-8"), hash_guardado):
            data.pop("contrasena", None)
            print("✅ Credenciales correctas")
            return data
        else:
            print("❌ Contraseña incorrecta")
            return None

    except Exception as e:
        print("Error en verificar_credenciales:", e)
        return None
