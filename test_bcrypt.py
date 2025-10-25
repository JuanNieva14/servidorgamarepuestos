import bcrypt
import mysql.connector

# Nueva contraseña que tú elijas
nueva_contrasena = "Juangama123"   # puedes cambiarla si quieres

# Generar el nuevo hash
hashed = bcrypt.hashpw(nueva_contrasena.encode("utf-8"), bcrypt.gensalt())
hash_str = hashed.decode("utf-8")

# Conectar a MySQL
conn = mysql.connector.connect(
        host="localhost",
        user="root",             
        password="123456",     
        database="respuestos_quibdo_corregido",
        port=3306                
    )
cursor = conn.cursor()

# Actualizar contraseña del usuario
cursor.execute(
    "UPDATE usuarios SET contrasena = %s WHERE usuario = %s",
    (hash_str, "juangonzalez")
)

conn.commit()
conn.close()

print("✅ Contraseña actualizada correctamente para 'juangonzalez'")
print("Hash guardado:", hash_str)
