from fastapi import APIRouter, HTTPException
from database import get_conn

router = APIRouter(prefix="/estados", tags=["Estados"])

@router.get("/")
def listar_estados():
    conexion = get_conn()
    cursor = conexion.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id_estado, nombre_estado FROM estados ORDER BY id_estado ASC;")
        return cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conexion.close()
