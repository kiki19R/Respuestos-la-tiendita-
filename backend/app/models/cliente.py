"""Modelo de Cliente"""

from datetime import datetime

from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Cliente(Base):
    """Modelo de cliente"""

    __tablename__ = "clientes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(255), index=True)
    cedula: Mapped[str] = mapped_column(String(20), unique=True, nullable=True, index=True)
    telefono: Mapped[str] = mapped_column(String(20), nullable=True)
    email: Mapped[str] = mapped_column(String(255), nullable=True)
    direccion: Mapped[str] = mapped_column(Text, nullable=True)
    tipo: Mapped[str] = mapped_column(
        String(50), default="Consumidor Final"
    )  # Consumidor Final, Empresa
    notas: Mapped[str] = mapped_column(Text, nullable=True)
    fecha_registro: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, index=True
    )
    fecha_actualizacion: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __repr__(self) -> str:
        return f"<Cliente(id={self.id}, nombre={self.nombre}, cedula={self.cedula})>"
