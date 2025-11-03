import mysql.connector
from datetime import datetime
from database import get_conn

# 💾 Insertar venta
def insertar_venta(id_cliente: int, id_usuario: int, id_forma_pago: int, productos: list):
    """
    Inserta una venta con sus productos en las tablas `facturas` y `detalle_facturas`.
    Calcula subtotal, impuesto (19%) y total automáticamente.
    """

    conn = get_conn()
    cursor = conn.cursor()

    try:
        # 🧮 Calcular subtotal, impuesto y total
        subtotal = sum(float(p["cantidad"]) * float(p["precio_unitario"]) for p in productos)
        impuesto = round(subtotal * 0.19, 2)
        total = round(subtotal + impuesto, 2)
        descuento = 0.00
        fecha_factura = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print(f"Insertando factura: Subtotal={subtotal}, IVA={impuesto}, Total={total}")

        # 🧾 Insertar factura (incluir todos los valores numéricos)
        cursor.execute("""
            INSERT INTO facturas (
                id_cliente, id_usuario, id_forma_pago, fecha_factura,
                subtotal, descuento, impuesto, total, id_estado
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            id_cliente, id_usuario, id_forma_pago, fecha_factura,
            subtotal, descuento, impuesto, total, 6
        ))

        id_factura = cursor.lastrowid

        # 📦 Insertar detalle de productos
        for p in productos:
            cursor.execute("""
                INSERT INTO detalle_facturas (
                    id_factura, id_producto, cantidad, precio_unitario
                ) VALUES (%s, %s, %s, %s)
            """, (
                id_factura,
                p["id_producto"],
                p["cantidad"],
                p["precio_unitario"]
            ))

        conn.commit()
        print(f"✅ Venta registrada correctamente (Factura ID: {id_factura})")

        return {
            "ok": True,
            "mensaje": "Venta registrada correctamente.",
            "id_factura": id_factura,
            "subtotal": subtotal,
            "impuesto": impuesto,
            "total": total
        }

    except Exception as e:
        print(f"❌ Error al registrar venta: {e}")
        conn.rollback()
        raise

    finally:
        cursor.close()
        conn.close()
