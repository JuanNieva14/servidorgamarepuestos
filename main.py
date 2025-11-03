from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 📦 Importación de los routers
from routers import (
    productos_router,
    categorias_router,
    personas_router,
    register_router,
    login_router,
    danos_router,
    formas_pago_router,
    estados_router,
    pedidos_router,
    proveedores_router,
    usuarios_router,
    inventario_router,
    registro_productos_router,
    clasificacion_router,
    ventasproductos_router,
    clientes_router,
    formaspagos_router,
    actualizar_stock_router,
    cotizaciones_router,
    consulta_productos_router,
    consulta_clientes_router,
)

# 🚀 Inicialización de la aplicación python -m uvicorn main:app --reload --port 8001
app = FastAPI(title="API Gama Repuestos Quibdó")

# 🌐 Configuración de CORS para permitir conexión desde React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes reemplazar "*" por ["http://localhost:5173"] si usas Vite
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🏠 Ruta raíz para verificar que la API funciona
@app.get("/")
def home():
    return {"mensaje": "✅ API Gama Repuestos Quibdó funcionando con todas las tablas"}

# 🔗 Conexión de todos los routers (endpoints)
app.include_router(productos_router.router)
app.include_router(categorias_router.router)
app.include_router(personas_router.router)
app.include_router(register_router.router)
app.include_router(login_router.router)
app.include_router(danos_router.router)
app.include_router(formas_pago_router.router)
app.include_router(estados_router.router)
app.include_router(pedidos_router.router)
app.include_router(proveedores_router.router)
app.include_router(usuarios_router.router)
app.include_router(inventario_router.router)
app.include_router(registro_productos_router.router)
app.include_router(clasificacion_router.router)
app.include_router(ventasproductos_router.router)
app.include_router(clientes_router.router)
app.include_router(formaspagos_router.router)
app.include_router(actualizar_stock_router.router)
app.include_router(cotizaciones_router.router)
app.include_router(consulta_productos_router.router)
app.include_router(consulta_clientes_router.router)
