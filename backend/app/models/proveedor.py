"""Modelo de Proveedor"""

from datetime import datetime

from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Proveedor(Base):
    """Modelo de proveedor"""

    __tablename__ = "proveedores"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(255), index=True)
    rif: Mapped[str] = mapped_column(String(20), unique=True, nullable=True, index=True)
    telefono: Mapped[str] = mapped_column(String(20), nullable=True)
    email: Mapped[str] = mapped_column(String(255), nullable=True)
    contacto: Mapped[str] = mapped_column(String(255), nullable=True)
    direccion: Mapped[str] = mapped_column(Text, nullable=True)
    notas: Mapped[str] = mapped_column(Text, nullable=True)
    activo: Mapped[bool] = mapped_column(default=True, index=True)
    fecha_registro: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, index=True
    )
    fecha_actualizacion: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __repr__(self) -> str:
        return f"<Proveedor(id={self.id}, nombre={self.nombre}, rif={self.rif})>"
