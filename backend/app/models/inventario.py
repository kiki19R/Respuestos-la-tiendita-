"""Modelo de Inventario"""

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Inventario(Base):
    """Modelo de control de inventario"""

    __tablename__ = "inventario"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    producto_id: Mapped[int] = mapped_column(
        ForeignKey("productos.id"), unique=True, index=True
    )
    cantidad: Mapped[int] = mapped_column(Integer, default=0, index=True)
    cantidad_minima: Mapped[int] = mapped_column(Integer, default=10)
    ubicacion: Mapped[str] = mapped_column(String(255), nullable=True)
    fecha_actualizacion: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __repr__(self) -> str:
        return f"<Inventario(producto_id={self.producto_id}, cantidad={self.cantidad})>"
