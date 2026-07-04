"""Agregador de todas las rutas API v1"""

from fastapi import APIRouter

from app.api.v1.endpoints import auth, clientes, productos, inventario, proveedores, health

api_router = APIRouter(prefix="/api/v1")

# Incluir routers
api_router.include_router(health.router)
api_router.include_router(auth.router)
api_router.include_router(clientes.router)
api_router.include_router(productos.router)
api_router.include_router(inventario.router)
api_router.include_router(proveedores.router)
