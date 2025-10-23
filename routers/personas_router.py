from fastapi import APIRouter
from typing import List
from database import get_conn

router = APIRouter(prefix="/personas", tags=["Personas"])

@router.get("/")
def listar_personas():
    try:
        conn = get_conn()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM personas")  # usa el nombre real de tu tabla
        data = cur.fetchall()
        conn.close()
        return data
    except Exception as e:
        return {"error": str(e)}

