from database import get_conn

def obtener_proveedores():
    conn = get_conn()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT
            pr.id_proveedor AS id_proveedor,
            pr.nit AS nit,
            CONCAT(p.nombre, ' ', p.apellido) AS nombre_completo,
            p.tipo_documento AS tipo_documento,
            p.numero_documento AS numero_documento,
            p.correo AS correo,
            p.direccion AS direccion,
            c.nombre_ciudad AS ciudad,
            DATE_FORMAT(p.fecha_creacion, '%Y-%m-%d %H:%i:%s') AS fecha_creacion,
            DATE_FORMAT(p.fecha_modificacion, '%Y-%m-%d %H:%i:%s') AS fecha_modificacion
        FROM proveedores pr
        INNER JOIN personas p ON pr.id_persona = p.id_persona
        LEFT JOIN ciudades c ON p.id_ciudad = c.id_ciudad
        ORDER BY pr.id_proveedor ASC
    """)
    data = cursor.fetchall()
    conn.close()
    return data


def agregar_proveedor(nit, nombre, apellido, tipo_documento, numero_documento, correo, direccion, id_ciudad):
    conn = get_conn()
    cursor = conn.cursor()

    # Crear persona asociada
    cursor.execute("""
        INSERT INTO personas (nombre, apellido, tipo_documento, numero_documento, correo, direccion, id_ciudad, fecha_creacion)
        VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
    """, (nombre, apellido, tipo_documento, numero_documento, correo, direccion, id_ciudad))
    id_persona = cursor.lastrowid

    # Crear proveedor vinculado
    cursor.execute("""
        INSERT INTO proveedores (nit, id_persona)
        VALUES (%s, %s)
    """, (nit, id_persona))

    conn.commit()
    conn.close()
    return {"ok": True, "mensaje": "Proveedor registrado correctamente"}


def actualizar_proveedor(id_proveedor, nit, nombre, apellido, tipo_documento, numero_documento, correo, direccion, id_ciudad):
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE personas
        INNER JOIN proveedores ON personas.id_persona = proveedores.id_persona
        SET personas.nombre = %s,
            personas.apellido = %s,
            personas.tipo_documento = %s,
            personas.numero_documento = %s,
            personas.correo = %s,
            personas.direccion = %s,
            personas.id_ciudad = %s,
            personas.fecha_modificacion = NOW(),
            proveedores.nit = %s
        WHERE proveedores.id_proveedor = %s
    """, (nombre, apellido, tipo_documento, numero_documento, correo, direccion, id_ciudad, nit, id_proveedor))

    conn.commit()
    conn.close()
    return {"ok": True, "mensaje": "Proveedor actualizado correctamente"}


def eliminar_proveedor(id_proveedor):
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM personas
        WHERE id_persona = (
            SELECT id_persona FROM proveedores WHERE id_proveedor = %s
        )
    """, (id_proveedor,))

    cursor.execute("DELETE FROM proveedores WHERE id_proveedor = %s", (id_proveedor,))
    conn.commit()
    conn.close()
    return {"ok": True, "mensaje": "Proveedor eliminado correctamente"}
