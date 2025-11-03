from fastapi import APIRouter, HTTPException
from database import get_conn

router = APIRouter(prefix="/formaspago", tags=["Formas de Pago"])

@router.get("")
def listar_formas_pago():
    try:
        conn = get_conn()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT id_forma_pago, nombre_forma
            FROM formas_pago
            WHERE activo = 1
            ORDER BY nombre_forma ASC
        """)
        data = cursor.fetchall()
        conn.close()
        return data
    except Exception as e:
        print("❌ Error al listar formas de pago:", e)
        raise HTTPException(status_code=500, detail=str(e))

