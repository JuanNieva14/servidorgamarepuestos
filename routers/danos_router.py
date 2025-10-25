from fastapi import APIRouter, HTTPException
from models.danos import get_conn, Dano, DanoDB

router = APIRouter(prefix="/danos", tags=["Daños"])

# 🧾 Obtener todos los registros
@router.get("/", response_model=list[DanoDB])
def listar_danos():
    conexion = get_conn()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos_danados ORDER BY fecha_registro DESC")
    danos = cursor.fetchall()
    conexion.close()
    return danos

# ➕ Agregar un nuevo daño
@router.post("/")
def agregar_dano(dano: Dano):
    conexion = get_conn()
    cursor = conexion.cursor()
    sql = "INSERT INTO productos_danados (id_producto, cantidad, motivo) VALUES (%s, %s, %s)"
    valores = (dano.id_producto, dano.cantidad, dano.motivo)
    cursor.execute(sql, valores)
    conexion.commit()
    conexion.close()
    return {"mensaje": "✅ Registro agregado correctamente."}

# ✏️ Actualizar daño
@router.put("/{id_dano}")
def actualizar_dano(id_dano: int, dano: Dano):
    conexion = get_conn()
    cursor = conexion.cursor()
    sql = "UPDATE productos_danados SET id_producto=%s, cantidad=%s, motivo=%s WHERE id_producto_danado=%s"
    valores = (dano.id_producto, dano.cantidad, dano.motivo, id_dano)
    cursor.execute(sql, valores)
    conexion.commit()
    conexion.close()
    return {"mensaje": "✅ Registro actualizado correctamente."}

# 🗑️ Eliminar daño
@router.delete("/{id_dano}")
def eliminar_dano(id_dano: int):
    conexion = get_conn()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM productos_danados WHERE id_producto_danado = %s", (id_dano,))
    conexion.commit()
    conexion.close()
    return {"mensaje": "🗑️ Registro eliminado correctamente."}
