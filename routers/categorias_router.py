from fastapi import APIRouter, HTTPException
from typing import List
from models.categorias import Categoria
from database import get_conn

router = APIRouter(prefix="/categorias", tags=["Categorías"])

@router.get("/", response_model=List[Categoria])
def listar_categorias():
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM categorias")
    data = cur.fetchall()
    conn.close()
    return data

@router.post("/")
def crear_categoria(c: Categoria):
    conn = get_conn()
    cur = conn.cursor()
    sql = "INSERT INTO categorias (nombre_categoria, descripcion, estado) VALUES (%s, %s, %s)"
    cur.execute(sql, (c.nombre_categoria, c.descripcion, c.estado))
    conn.commit()
    conn.close()
    return {"mensaje": "Categoría creada exitosamente"}

@router.put("/{id_categoria}")
def actualizar_categoria(id_categoria: int, c: Categoria):
    conn = get_conn()
    cur = conn.cursor()
    sql = "UPDATE categorias SET nombre_categoria=%s, descripcion=%s, estado=%s WHERE id_categoria=%s"
    cur.execute(sql, (c.nombre_categoria, c.descripcion, c.estado, id_categoria))
    conn.commit()
    conn.close()
    return {"mensaje": "Categoría actualizada exitosamente"}
