"""Configuración y conexión a la base de datos"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import get_settings

config = get_settings()

# Crear engine de SQLAlchemy
engine = create_engine(
    config.database_url,
    echo=config.debug,  # Mostrar SQL en logs si debug=True
    pool_pre_ping=True,  # Verificar conexión antes de usarla
)

# Crear session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()


def get_db():
    """Dependencia para obtener sesión de BD en endpoints"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
