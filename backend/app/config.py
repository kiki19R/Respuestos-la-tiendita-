"""Configuración de la aplicación FastAPI"""

from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configuración de la aplicación desde variables de entorno"""

    # Aplicación
    app_name: str = "Respuestos La Tiendita"
    app_version: str = "1.0.0"
    debug: bool = False

    # Base de Datos
    database_url: str = "postgresql://user:password@localhost:5432/respuestos_db"

    # Seguridad
    secret_key: str = "tu-secret-key-cambiar-en-produccion"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    # CORS
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:5173"]

    # Email
    smtp_server: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""

    # Redis
    redis_url: str = "redis://localhost:6379"

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Obtiene la configuración (cached)"""
    return Settings()
