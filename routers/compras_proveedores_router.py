from fastapi import APIRouter
from models.compras_proveedores import router as compras_router

router = APIRouter()
router.include_router(compras_router, prefix="", tags=["Compras Proveedores"])
