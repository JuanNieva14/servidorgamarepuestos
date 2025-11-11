from fastapi import APIRouter, HTTPException
from models.gestion_pedidos_proveedores import PedidoProveedor
from database import get_conn

router = APIRouter(prefix="/pedidos_proveedores", tags=["Pedidos Proveedores"])


# ➕ Crear pedido
from fastapi import APIRouter, HTTPException
from models.gestion_pedidos_proveedores import PedidoProveedor
from database import get_conn

router = APIRouter(prefix="/pedidos_proveedores", tags=["Pedidos Proveedores"])


# 🟢 Crear pedido
@router.post("")
def crear_pedido(pedido: PedidoProveedor):
    try:
        conn = get_conn()
        cursor = conn.cursor()

        # Si algún campo no se envía, asignamos None (NULL en SQL)
        id_proveedor = pedido.id_proveedor if pedido.id_proveedor else None
        id_usuario = pedido.id_usuario if pedido.id_usuario else None
        id_estado = pedido.id_estado if pedido.id_estado else None

        cursor.execute("""
            INSERT INTO pedidos_proveedores (
                numero_pedido,
                id_proveedor,
                id_usuario,
                fecha_pedido,
                fecha_entrega_esperada,
                id_estado,
                total,
                observaciones
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            pedido.numero_pedido,
            id_proveedor,
            id_usuario,
            pedido.fecha_pedido,
            pedido.fecha_entrega_esperada,
            id_estado,
            pedido.total,
            pedido.observaciones
        ))

        conn.commit()
        conn.close()
        return {"ok": True, "mensaje": "✅ Pedido creado correctamente."}

    except Exception as e:
        print("❌ Error al crear pedido:", e)
        raise HTTPException(status_code=500, detail=f"Error al crear pedido: {e}")


# 📋 Listar pedidos
@router.get("")
def listar_pedidos():
    try:
        conn = get_conn()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT 
                pp.id_pedido,
                pp.numero_pedido,
                CONCAT(per.nombre, ' ', per.apellido) AS proveedor,
                u.usuario AS vendedor,                     -- ✅ reemplazado aquí
                e.nombre_estado AS estado,
                pp.fecha_pedido,
                pp.fecha_entrega_esperada AS entrega,
                pp.total,
                pp.observaciones
            FROM pedidos_proveedores pp
            LEFT JOIN proveedores p ON pp.id_proveedor = p.id_proveedor
            LEFT JOIN personas per ON p.id_persona = per.id_persona
            LEFT JOIN usuarios u ON pp.id_usuario = u.id_usuario
            LEFT JOIN estados e ON pp.id_estado = e.id_estado
            ORDER BY pp.id_pedido DESC
        """)

        data = cursor.fetchall()
        conn.close()
        return {"success": True, "data": data}

    except Exception as e:
        print("❌ Error al listar pedidos:", e)
        raise HTTPException(status_code=500, detail=f"Error al listar pedidos: {e}")


# ✏️ Actualizar pedido
@router.put("/{id_pedido}")
def actualizar_pedido(id_pedido: int, pedido: PedidoProveedor):
    try:
        conn = get_conn()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE pedidos_proveedores
            SET 
                numero_pedido=%s,
                id_proveedor=%s,
                id_usuario=%s,
                fecha_pedido=%s,
                fecha_entrega_esperada=%s,
                id_estado=%s,
                total=%s,
                observaciones=%s
            WHERE id_pedido=%s
        """, (
            pedido.numero_pedido,
            pedido.id_proveedor,
            pedido.id_usuario,
            pedido.fecha_pedido,
            pedido.fecha_entrega_esperada,
            pedido.id_estado,
            pedido.total,
            pedido.observaciones,
            id_pedido
        ))

        conn.commit()
        conn.close()

        return {"ok": True, "mensaje": "Pedido actualizado correctamente."}

    except Exception as e:
        print("❌ Error al actualizar pedido:", e)
        raise HTTPException(status_code=500, detail=f"Error al actualizar pedido: {e}")


# 🗑️ Eliminar pedido
@router.delete("/{id_pedido}")
def eliminar_pedido(id_pedido: int):
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM pedidos_proveedores WHERE id_pedido=%s", (id_pedido,))
        conn.commit()
        conn.close()
        return {"ok": True, "mensaje": "Pedido eliminado correctamente."}
    except Exception as e:
        print("❌ Error al eliminar pedido:", e)
        raise HTTPException(status_code=500, detail=f"Error al eliminar pedido: {e}")
