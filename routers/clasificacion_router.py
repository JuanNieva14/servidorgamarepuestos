from fastapi import APIRouter, HTTPException
from models.clasificacion import Clasificacion
from database import get_conn
from datetime import datetime

router = APIRouter(prefix="/clasificaciones", tags=["Clasificaciones"])

# ➕ Crear clasificación
@router.post("")
def crear_clasificacion(clasificacion: Clasificacion):
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO clasificaciones (nombre_clasificacion, tipo, activo)
            VALUES (%s, %s, %s)
        """, (
            clasificacion.nombre_clasificacion,
            clasificacion.tipo,
            clasificacion.activo
        ))
        conn.commit()
        conn.close()
        return {"ok": True, "mensaje": "Clasificación creada correctamente."}
    except Exception as e:
        print("❌ Error al crear clasificación:", e)
        raise HTTPException(status_code=500, detail=f"Error al crear clasificación: {e}")

# 📋 Listar todas
@router.get("")
def listar_clasificaciones():
    try:
        conn = get_conn()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                id_clasificacion,
                nombre_clasificacion,
                COALESCE(tipo, '-') AS tipo,
                activo
            FROM clasificaciones
            ORDER BY id_clasificacion ASC
        """)
        data = cursor.fetchall()
        conn.close()
        return data
    except Exception as e:
        print("❌ Error al listar clasificaciones:", e)
        raise HTTPException(status_code=500, detail="Error al listar clasificaciones.")

# ✏️ Actualizar
@router.put("/{id_clasificacion}")
def actualizar_clasificacion(id_clasificacion: int, clasificacion: Clasificacion):
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE clasificaciones
            SET nombre_clasificacion=%s, tipo=%s, activo=%s
            WHERE id_clasificacion=%s
        """, (
            clasificacion.nombre_clasificacion,
            clasificacion.tipo,
            clasificacion.activo,
            id_clasificacion
        ))
        conn.commit()
        conn.close()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Clasificación no encontrada.")
        return {"ok": True, "mensaje": "Clasificación actualizada correctamente."}
    except Exception as e:
        print("❌ Error al actualizar clasificación:", e)
        raise HTTPException(status_code=500, detail=f"Error al actualizar clasificación: {e}")

# 📴 Desactivar
@router.put("/desactivar/{id_clasificacion}")
def desactivar_clasificacion(id_clasificacion: int):
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("UPDATE clasificaciones SET activo=0 WHERE id_clasificacion=%s", (id_clasificacion,))
        conn.commit()
        conn.close()
        return {"ok": True, "mensaje": "Clasificación desactivada correctamente."}
    except Exception as e:
        print("❌ Error al desactivar clasificación:", e)
        raise HTTPException(status_code=500, detail=str(e))

# 🔄 Activar
@router.put("/activar/{id_clasificacion}")
def activar_clasificacion(id_clasificacion: int):
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("UPDATE clasificaciones SET activo=1 WHERE id_clasificacion=%s", (id_clasificacion,))
        conn.commit()
        conn.close()
        return {"ok": True, "mensaje": "Clasificación activada correctamente."}
    except Exception as e:
        print("❌ Error al activar clasificación:", e)
        raise HTTPException(status_code=500, detail=str(e))

# 🗑️ Eliminar definitivamente
@router.delete("/eliminar/{id_clasificacion}")
def eliminar_clasificacion(id_clasificacion: int):
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM clasificaciones WHERE id_clasificacion=%s", (id_clasificacion,))
        conn.commit()
        conn.close()
        return {"ok": True, "mensaje": "Clasificación eliminada correctamente."}
    except Exception as e:
        print("❌ Error al eliminar clasificación:", e)
        raise HTTPException(status_code=500, detail=str(e))
