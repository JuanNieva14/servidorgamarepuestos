from fastapi import APIRouter, HTTPException
from models.pedidos import Pedido
from database import get_conn
import datetime, random

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])

def generar_numero_pedido():
    fecha = datetime.datetime.now().strftime("%Y%m%d")
    aleatorio = random.randint(100, 999)
    return f"PED-{fecha}-{aleatorio}"

@router.get("/")
def listar_pedidos():
    conexion = get_conn()
    cursor = conexion.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT 
                ped.id_pedido,
                ped.numero_pedido AS Numero_Pedido,
                CONCAT(perp.nombre, ' ', perp.apellido) AS Proveedor,
                u.usuario AS Usuario_Responsable,
                DATE(ped.fecha_pedido) AS Fecha_Pedido,
                DATE(ped.fecha_entrega_esperada) AS Fecha_Entrega_Esperada,
                e.nombre_estado AS Estado,
                FORMAT(ped.total, 0, 'es_CO') AS Total_COP,
                ped.observaciones,
                DATE(ped.fecha_registro) AS Fecha_Registro
            FROM pedidos_proveedores ped
            INNER JOIN proveedores pr ON ped.id_proveedor = pr.id_proveedor
            INNER JOIN personas perp ON pr.id_persona = perp.id_persona
            INNER JOIN usuarios u ON ped.id_usuario = u.id_usuario
            INNER JOIN estados e ON ped.id_estado = e.id_estado
            ORDER BY ped.fecha_pedido DESC;
        """)
        return cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conexion.close()

@router.post("/")
def crear_pedido(pedido: Pedido):
    conexion = get_conn()
    cursor = conexion.cursor()
    try:
        # ⚙️ Validar proveedor
        cursor.execute("SELECT id_proveedor FROM proveedores WHERE id_proveedor = %s", (pedido.id_proveedor,))
        if cursor.fetchone() is None:
            raise HTTPException(status_code=400, detail=f"El proveedor con ID {pedido.id_proveedor} no existe.")

        # ⚙️ Validar usuario
        cursor.execute("SELECT id_usuario FROM usuarios WHERE id_usuario = %s", (pedido.id_usuario,))
        if cursor.fetchone() is None:
            raise HTTPException(status_code=400, detail=f"El usuario con ID {pedido.id_usuario} no existe.")

        # ⚙️ Validar estado
        cursor.execute("SELECT id_estado FROM estados WHERE id_estado = %s", (pedido.id_estado,))
        if cursor.fetchone() is None:
            raise HTTPException(status_code=400, detail=f"El estado con ID {pedido.id_estado} no existe.")

        numero_pedido = generar_numero_pedido()
        fecha_actual = datetime.date.today()

        cursor.execute("""
            INSERT INTO pedidos_proveedores
            (numero_pedido, id_proveedor, id_usuario, id_estado, fecha_pedido, fecha_entrega_esperada, total, observaciones)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            numero_pedido,
            pedido.id_proveedor,
            pedido.id_usuario,
            pedido.id_estado,
            fecha_actual,
            pedido.fecha_entrega_esperada,
            pedido.total,
            pedido.observaciones
        ))
        conexion.commit()

        return {"mensaje": "✅ Pedido creado correctamente", "numero_pedido": numero_pedido}
    except Exception as e:
        conexion.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conexion.close()

@router.put("/{id_pedido}")
def actualizar_pedido(id_pedido: int, pedido: Pedido):
    conexion = get_conn()
    cursor = conexion.cursor()
    try:
        cursor.execute("""
            UPDATE pedidos_proveedores
            SET id_proveedor=%s, id_usuario=%s, id_estado=%s,
                fecha_entrega_esperada=%s, total=%s, observaciones=%s
            WHERE id_pedido=%s
        """, (
            pedido.id_proveedor,
            pedido.id_usuario,
            pedido.id_estado,
            pedido.fecha_entrega_esperada,
            pedido.total,
            pedido.observaciones,
            id_pedido
        ))
        conexion.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Pedido no encontrado")

        return {"mensaje": "✏️ Pedido actualizado correctamente"}
    except Exception as e:
        conexion.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conexion.close()

@router.delete("/{id_pedido}")
def eliminar_pedido(id_pedido: int):
    conexion = get_conn()
    cursor = conexion.cursor()
    try:
        cursor.execute("DELETE FROM pedidos_proveedores WHERE id_pedido=%s", (id_pedido,))
        conexion.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Pedido no encontrado")

        return {"mensaje": "🗑️ Pedido eliminado correctamente"}
    except Exception as e:
        conexion.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conexion.close()
