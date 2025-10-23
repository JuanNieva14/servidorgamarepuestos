from fastapi import APIRouter, HTTPException
from typing import List
from models.productos import Producto
from database import get_conn

router = APIRouter(prefix="/productos", tags=["Productos"])

@router.get("/", response_model=List[Producto])
def listar_productos():
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM productos")
    data = cur.fetchall()
    conn.close()
    return data

@router.post("/")
def crear_producto(p: Producto):
    conn = get_conn()
    cur = conn.cursor()
    sql = """
        INSERT INTO productos (nombre_producto, precio_venta, descripcion, id_categoria, id_estado)
        VALUES (%s, %s, %s, %s, %s)
    """
    cur.execute(sql, (p.nombre_producto, p.precio_venta, p.descripcion, p.id_categoria, p.id_estado))
    conn.commit()
    conn.close()
    return {"mensaje": "Producto creado exitosamente"}

@router.put("/{id_producto}")
def actualizar_producto(id_producto: int, p: Producto):
    conn = get_conn()
    cur = conn.cursor()
    sql = """
        UPDATE productos
        SET nombre_producto=%s, precio_venta=%s, descripcion=%s, id_categoria=%s, id_estado=%s
        WHERE id_producto=%s
    """
    cur.execute(sql, (p.nombre_producto, p.precio_venta, p.descripcion, p.id_categoria, p.id_estado, id_producto))
    conn.commit()
    conn.close()
    return {"mensaje": "Producto actualizado exitosamente"}

@router.delete("/{id_producto}")
def eliminar_producto(id_producto: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM productos WHERE id_producto=%s", (id_producto,))
    conn.commit()
    conn.close()
    return {"mensaje": "Producto eliminado exitosamente"}
