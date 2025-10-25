from pydantic import BaseModel
from database import get_conn

class Estado(BaseModel):
    nombre_estado: str
    tipo_estado: str

def obtener_todos():
    conexion = get_conn()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM estados ORDER BY id_estado ASC")
    resultados = cursor.fetchall()
    conexion.close()
    return resultados

def crear_estado(estado: Estado):
    conexion = get_conn()
    cursor = conexion.cursor()
    cursor.execute(
        "INSERT INTO estados (nombre_estado, tipo_estado) VALUES (%s, %s)",
        (estado.nombre_estado, estado.tipo_estado)
    )
    conexion.commit()
    conexion.close()

def actualizar_estado(id_estado: int, estado: Estado):
    conexion = get_conn()
    cursor = conexion.cursor()
    cursor.execute(
        "UPDATE estados SET nombre_estado=%s, tipo_estado=%s WHERE id_estado=%s",
        (estado.nombre_estado, estado.tipo_estado, id_estado)
    )
    conexion.commit()
    conexion.close()

def eliminar_estado(id_estado: int):
    conexion = get_conn()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM estados WHERE id_estado=%s", (id_estado,))
    conexion.commit()
    conexion.close()

def obtener_por_id(id_estado: int):
    conexion = get_conn()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM estados WHERE id_estado=%s", (id_estado,))
    resultado = cursor.fetchone()
    conexion.close()
    return resultado
