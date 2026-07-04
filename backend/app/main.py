"""Aplicación principal FastAPI actualizada"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.core.logging import app_logger
from app.api.v1.router import api_router

config = get_settings()

# Crear aplicación
app = FastAPI(
    title=config.app_name,
    version=config.app_version,
    description="API profesional para gestión de respuestos",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(api_router)


# Rutas de health check
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "version": config.app_version}


@app.get("/", tags=["Info"])
async def api_info():
    """Información de la API"""
    return {
        "name": config.app_name,
        "version": config.app_version,
        "docs": "/api/docs",
        "endpoints": [
            "/api/v1/auth/login",
            "/api/v1/auth/registro",
            "/api/v1/clientes",
            "/api/v1/productos",
            "/api/v1/inventario",
            "/api/v1/proveedores",
        ]
    }


# Event listeners
@app.on_event("startup")
async def startup_event():
    """Evento de inicio de la aplicación"""
    app_logger.info(f"✅ {config.app_name} iniciada - Versión {config.app_version}")


@app.on_event("shutdown")
async def shutdown_event():
    """Evento de cierre de la aplicación"""
    app_logger.info("❌ Aplicación cerrada")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=config.debug,
        log_level="info",
    )
