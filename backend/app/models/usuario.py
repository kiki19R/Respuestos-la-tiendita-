"""Modelo de Usuario"""

from datetime import datetime

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Usuario(Base):
    """Modelo de usuario del sistema"""

    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    nombre_completo: Mapped[str] = mapped_column(String(255))
    contraseña_hash: Mapped[str] = mapped_column(String(255))
    activo: Mapped[bool] = mapped_column(Boolean, default=True)
    rol: Mapped[str] = mapped_column(String(50), default="vendedor")  # admin, gerente, vendedor
    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, index=True
    )
    fecha_actualizacion: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __repr__(self) -> str:
        return f"<Usuario(id={self.id}, email={self.email}, nombre={self.nombre_completo})>"
