"""Modelo de Compra"""

from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Compra(Base):
    """Modelo de compra a proveedor"""

    __tablename__ = "compras"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    numero_compra: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    proveedor_id: Mapped[int] = mapped_column(ForeignKey("proveedores.id"), index=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), index=True)
    fecha_compra: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, index=True
    )
    total: Mapped[float] = mapped_column(Float, default=0)
    estado: Mapped[str] = mapped_column(
        String(50), default="Pendiente"
    )  # Pendiente, Completada, Cancelada
    notas: Mapped[str] = mapped_column(Text, nullable=True)

    # Relaciones
    detalles = relationship(
        "DetalleCompra", back_populates="compra", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Compra(id={self.id}, numero_compra={self.numero_compra}, total={self.total})>"


class DetalleCompra(Base):
    """Modelo de detalle de compra"""

    __tablename__ = "detalles_compra"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    compra_id: Mapped[int] = mapped_column(ForeignKey("compras.id"), index=True)
    producto_id: Mapped[int] = mapped_column(ForeignKey("productos.id"), index=True)
    cantidad: Mapped[int] = mapped_column(default=1)
    precio_unitario: Mapped[float] = mapped_column(Float)
    subtotal: Mapped[float] = mapped_column(Float)

    # Relaciones
    compra = relationship("Compra", back_populates="detalles")

    def __repr__(self) -> str:
        return f"<DetalleCompra(compra_id={self.compra_id}, producto_id={self.producto_id}, cantidad={self.cantidad})>"
