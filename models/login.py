import bcrypt
from database import get_conn  # asegúrate de que tu archivo database.py tenga esta función

def verificar_credenciales(usuario: str, contrasena: str):
    """
    Verifica las credenciales de inicio de sesión.
    Retorna los datos del usuario si son válidos, o None si no coinciden.
    """
    try:
        conn = get_conn()
        cursor = conn.cursor(dictionary=True)

        # 🔹 Consulta adaptada a tu base de datos
        cursor.execute("""
            SELECT 
                u.id_usuario,
                p.numero_documento,
                u.usuario AS nombre_usuario,
                u.contrasena AS hash,
                p.nombre AS nombre_persona,
                p.apellido,
                p.correo AS email,
                r.nombre_rol AS rol,
                u.activo
            FROM usuarios u
            LEFT JOIN personas p ON u.id_persona = p.id_persona
            LEFT JOIN roles r ON u.id_rol = r.id_rol
            WHERE u.usuario = %s AND u.activo = 1
        """, (usuario,))

        data = cursor.fetchone()
        cursor.close()
        conn.close()

        if not data:
            print("⚠️ Usuario no encontrado en la base de datos.")
            return None

        # 🔐 Corrige compatibilidad entre $2y$ (PHP) y $2b$ (Python)
        hash_guardado = data["hash"].encode("utf-8").replace(b"$2y$", b"$2b$")

        # 🔑 Verificar contraseña
        if bcrypt.checkpw(contrasena.encode("utf-8"), hash_guardado):
            print("✅ Credenciales correctas para:", data["nombre_usuario"])

            # Eliminamos el hash antes de enviar al frontend
            data.pop("hash", None)
            return {
                "id_usuario": data["id_usuario"],
                "usuario": data["nombre_usuario"],
                "nombre": data["nombre_persona"],
                "apellido": data["apellido"],
                "documento": data["numero_documento"],
                "correo": data["email"],
                "rol": data["rol"]
            }

        else:
            print("❌ Contraseña incorrecta para usuario:", usuario)
            return None

    except Exception as e:
        print("🚨 Error en verificar_credenciales:", e)
        return None
