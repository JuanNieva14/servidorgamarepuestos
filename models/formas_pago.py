from pydantic import BaseModel
from database import get_conn


# 🔹 Modelo Pydantic
class FormaPago(BaseModel):
    nombre_forma: str
    descripcion: str
    activo: int = 1

# 🔹 Consultas SQL
def obtener_todos():
    conexion = get_conn()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM formas_pago ORDER BY id_forma_pago ASC")
    resultados = cursor.fetchall()
    conexion.close()
    return resultados

def crear_forma_pago(forma: FormaPago):
    conexion = get_conn()
    cursor = conexion.cursor()
    cursor.execute(
        "INSERT INTO formas_pago (nombre_forma, descripcion, activo) VALUES (%s, %s, %s)",
        (forma.nombre_forma, forma.descripcion, forma.activo)
    )
    conexion.commit()
    conexion.close()

def actualizar_forma_pago(id_forma_pago: int, forma: FormaPago):
    conexion = get_conn()
    cursor = conexion.cursor()
    cursor.execute(
        "UPDATE formas_pago SET nombre_forma=%s, descripcion=%s, activo=%s WHERE id_forma_pago=%s",
        (forma.nombre_forma, forma.descripcion, forma.activo, id_forma_pago)
    )
    conexion.commit()
    conexion.close()

def eliminar_forma_pago(id_forma_pago: int):
    conexion = get_conn()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM formas_pago WHERE id_forma_pago=%s", (id_forma_pago,))
    conexion.commit()
    conexion.close()

def obtener_por_id(id_forma_pago: int):
    conexion = get_conn()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM formas_pago WHERE id_forma_pago=%s", (id_forma_pago,))
    resultado = cursor.fetchone()
    conexion.close()
    return resultado
