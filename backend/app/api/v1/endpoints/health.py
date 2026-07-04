"""Endpoint de verificación de salud de la API"""

from fastapi import APIRouter
from datetime import datetime

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health_check():
    """Verificar salud de la API"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
    }
