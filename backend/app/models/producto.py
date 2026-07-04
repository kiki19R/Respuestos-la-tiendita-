"""Modelo de Producto"""

from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Producto(Base):
    """Modelo de producto"""

    __tablename__ = "productos"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    codigo: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    nombre: Mapped[str] = mapped_column(String(255), index=True)
    descripcion: Mapped[str] = mapped_column(Text, nullable=True)
    precio_compra: Mapped[float] = mapped_column(Float, nullable=True)
    precio_venta: Mapped[float] = mapped_column(Float, index=True)
    proveedor_id: Mapped[int] = mapped_column(
        ForeignKey("proveedores.id"), nullable=True, index=True
    )
    activo: Mapped[bool] = mapped_column(default=True, index=True)
    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, index=True
    )
    fecha_actualizacion: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __repr__(self) -> str:
        return f"<Producto(id={self.id}, codigo={self.codigo}, nombre={self.nombre})>"
