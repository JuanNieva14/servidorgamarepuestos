from database import get_conn

# 📋 Listar todos los pedidos
def listar_pedidos_proveedores():
    try:
        conn = get_conn()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                pp.id_pedido,
                CONCAT(pv.nombre, ' ', pv.apellido) AS proveedor,
                CONCAT(v.nombre, ' ', v.apellido) AS vendedor,
                pr.nombre_producto AS producto,
                e.nombre_estado AS estado,
                pp.fecha_pedido,
                pp.fecha_entrega,
                pp.total,
                pp.observacion
            FROM pedidos_proveedores pp
            INNER JOIN proveedores prv ON pp.id_proveedor = prv.id_proveedor
            INNER JOIN personas pv ON prv.id_persona = pv.id_persona
            INNER JOIN usuarios u ON pp.id_usuario = u.id_usuario
            INNER JOIN personas v ON u.id_persona = v.id_persona
            INNER JOIN productos pr ON pp.id_producto = pr.id_producto
            INNER JOIN estados e ON pp.id_estado = e.id_estado
            ORDER BY pp.fecha_pedido DESC
        """)
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return {"success": True, "data": data}
    except Exception as e:
        return {"success": False, "error": f"Error al listar pedidos: {e}"}

# 🆕 Crear pedido
def crear_pedido_proveedor(data: dict):
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO pedidos_proveedores
            (id_proveedor, id_usuario, id_producto, fecha_pedido, fecha_entrega, id_estado, total, observacion)
            VALUES (%s, %s, %s, NOW(), %s, %s, %s, %s)
        """, (
            data["id_proveedor"],
            data["id_usuario"],
            data["id_producto"],
            data["fecha_entrega"],
            data["id_estado"],
            data["total"],
            data["observacion"],
        ))
        conn.commit()
        cursor.close()
        conn.close()
        return {"success": True, "message": "Pedido creado correctamente"}
    except Exception as e:
        return {"success": False, "error": f"Error al crear pedido: {e}"}

# ✏️ Actualizar pedido (solo observación y total)
def actualizar_pedido_proveedor(id_pedido: int, data: dict):
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE pedidos_proveedores
            SET total = %s, observacion = %s
            WHERE id_pedido = %s
        """, (data["total"], data["observacion"], id_pedido))
        conn.commit()
        cursor.close()
        conn.close()
        return {"success": True, "message": "Pedido actualizado correctamente"}
    except Exception as e:
        return {"success": False, "error": f"Error al actualizar pedido: {e}"}

# 🗑️ Eliminar pedido
def eliminar_pedido_proveedor(id_pedido: int):
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM pedidos_proveedores WHERE id_pedido = %s", (id_pedido,))
        conn.commit()
        cursor.close()
        conn.close()
        return {"success": True, "message": "Pedido eliminado correctamente"}
    except Exception as e:
        return {"success": False, "error": f"Error al eliminar pedido: {e}"}

# 📦 Proveedores
def listar_proveedores_select():
    try:
        conn = get_conn()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                prv.id_proveedor, 
                CONCAT(p.nombre, ' ', p.apellido) AS nombre
            FROM proveedores prv
            INNER JOIN personas p ON prv.id_persona = p.id_persona
            ORDER BY p.nombre ASC
        """)
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return {"success": True, "data": data}
    except Exception as e:
        return {"success": False, "error": f"Error al listar proveedores: {e}"}

# 👨‍💼 Vendedores
def listar_vendedores_select():
    try:
        conn = get_conn()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                u.id_usuario,
                CONCAT(p.nombre, ' ', p.apellido) AS nombre
            FROM usuarios u
            INNER JOIN personas p ON u.id_persona = p.id_persona
            WHERE u.activo = 1
            ORDER BY p.nombre ASC
        """)
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return {"success": True, "data": data}
    except Exception as e:
        return {"success": False, "error": f"Error al listar vendedores: {e}"}

# 🧾 Estados
def listar_estados_select():
    try:
        conn = get_conn()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id_estado, nombre_estado FROM estados ORDER BY nombre_estado ASC")
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return {"success": True, "data": data}
    except Exception as e:
        return {"success": False, "error": f"Error al listar estados: {e}"}
