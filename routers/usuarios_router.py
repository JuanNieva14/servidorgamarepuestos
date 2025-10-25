from fastapi import APIRouter, HTTPException
from database import get_conn

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

@router.get("/")
def listar_usuarios():
    conexion = get_conn()
    cursor = conexion.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id_usuario, usuario FROM usuarios ORDER BY usuario ASC;")
        return cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conexion.close()
