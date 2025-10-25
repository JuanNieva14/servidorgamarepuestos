from fastapi import APIRouter, HTTPException
from database import get_conn

router = APIRouter(prefix="/proveedores", tags=["Proveedores"])

@router.get("/")
def listar_proveedores():
    conexion = get_conn()
    cursor = conexion.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT 
                pr.id_proveedor,
                CONCAT(per.nombre, ' ', per.apellido) AS nombre
            FROM proveedores pr
            INNER JOIN personas per ON pr.id_persona = per.id_persona
            ORDER BY nombre ASC;
        """)
        return cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conexion.close()
