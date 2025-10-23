from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import (
    productos_router,
    categorias_router,
    personas_router
    # 👉 agrega aquí el resto de tus routers
)

app = FastAPI(title="API Gama Repuestos Quibdó")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"mensaje": "✅ API Gama Repuestos Quibdó funcionando con todas las tablas"}

# 🔗 Conexión de routers
app.include_router(productos_router.router)
app.include_router(categorias_router.router)
app.include_router(personas_router.router)
