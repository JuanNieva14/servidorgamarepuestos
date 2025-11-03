from fastapi import APIRouter, HTTPException
from database import get_conn

router = APIRouter(prefix="/clientes", tags=["Clientes"])

@router.get("/")
def listar_clientes():
    conn = get_conn()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            c.id_cliente, 
            p.nombre, 
            p.apellido 
        FROM clientes c
        INNER JOIN personas p ON c.id_persona = p.id_persona
        ORDER BY p.nombre ASC
    """)
    data = cursor.fetchall()
    conn.close()
    return data


