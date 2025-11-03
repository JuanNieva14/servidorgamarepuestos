from fastapi import APIRouter, HTTPException
from models.categorias import Categoria, get_conn
from datetime import datetime

router = APIRouter(prefix="/categorias", tags=["Categorías"])

# ➕ Crear categoría
@router.post("")
def crear_categoria(categoria: Categoria):
    try:
        conn = get_conn()
        cursor = conn.cursor()
        ahora = datetime.now()
        cursor.execute(
            "INSERT INTO categorias (nombre_categoria, activo, fecha_creacion, fecha_modificacion) VALUES (%s, %s, %s, %s)",
            (categoria.nombre_categoria, 1, ahora, ahora)
        )
        conn.commit()
        conn.close()
        return {"ok": True, "mensaje": "✅ Categoría creada correctamente."}
    except Exception as e:
        print("❌ Error al crear categoría:", e)
        raise HTTPException(status_code=500, detail="❌ Error al crear la categoría.")

# 📋 Listar todas
@router.get("")
def listar_categorias():
    try:
        conn = get_conn()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM categorias ORDER BY id_categoria ASC")
        data = cursor.fetchall()
        conn.close()
        return data
    except Exception as e:
        print("❌ Error al listar categorías:", e)
        raise HTTPException(status_code=500, detail="❌ Error al listar las categorías.")

# ✏️ Actualizar
@router.put("/{id_categoria}")
def actualizar_categoria(id_categoria: int, categoria: Categoria):
    try:
        conn = get_conn()
        cursor = conn.cursor()
        ahora = datetime.now()
        cursor.execute(
            "UPDATE categorias SET nombre_categoria=%s, activo=%s, fecha_modificacion=%s WHERE id_categoria=%s",
            (categoria.nombre_categoria, categoria.activo, ahora, id_categoria)
        )
        conn.commit()
        conn.close()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="❌ Categoría no encontrada.")
        return {"ok": True, "mensaje": "✅ Categoría actualizada correctamente."}
    except Exception as e:
        print("❌ Error al actualizar categoría:", e)
        raise HTTPException(status_code=500, detail="❌ Error al actualizar la categoría.")

# 📴 Desactivar
@router.delete("/{id_categoria}")
def desactivar_categoria(id_categoria: int):
    try:
        conn = get_conn()
        cursor = conn.cursor()
        ahora = datetime.now()
        cursor.execute(
            "UPDATE categorias SET activo=0, fecha_modificacion=%s WHERE id_categoria=%s",
            (ahora, id_categoria)
        )
        conn.commit()
        conn.close()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="❌ Categoría no encontrada.")
        return {"ok": True, "mensaje": "⚠️ Categoría desactivada correctamente."}
    except Exception as e:
        print("❌ Error al desactivar categoría:", e)
        raise HTTPException(status_code=500, detail="❌ Error al desactivar la categoría.")

# 🔄 Activar
@router.put("/activar/{id_categoria}")
def activar_categoria(id_categoria: int):
    try:
        conn = get_conn()
        cursor = conn.cursor()
        ahora = datetime.now()
        cursor.execute(
            "UPDATE categorias SET activo=1, fecha_modificacion=%s WHERE id_categoria=%s",
            (ahora, id_categoria)
        )
        conn.commit()
        conn.close()
        return {"ok": True, "mensaje": "✅ Categoría activada correctamente."}
    except Exception as e:
        print("❌ Error al activar categoría:", e)
        raise HTTPException(status_code=500, detail="❌ Error al activar la categoría.")

# 🗑️ Eliminar definitivamente
@router.delete("/eliminar/{id_categoria}")
def eliminar_categoria(id_categoria: int):
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM categorias WHERE id_categoria=%s", (id_categoria,))
        conn.commit()
        conn.close()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="❌ Categoría no encontrada.")
        return {"ok": True, "mensaje": "🗑️ Categoría eliminada correctamente."}
    except Exception as e:
        print("❌ Error al eliminar categoría:", e)
        raise HTTPException(status_code=500, detail="❌ Error al eliminar la categoría.")
