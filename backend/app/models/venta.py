"""Modelo de Venta"""

from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Venta(Base):
    """Modelo de venta"""

    __tablename__ = "ventas"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    numero_factura: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    cliente_id: Mapped[int] = mapped_column(
        ForeignKey("clientes.id"), nullable=True, index=True
    )
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), index=True)
    fecha_venta: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, index=True
    )
    subtotal: Mapped[float] = mapped_column(Float, default=0)
    descuento: Mapped[float] = mapped_column(Float, default=0)
    total: Mapped[float] = mapped_column(Float, default=0)
    pago_recibido: Mapped[float] = mapped_column(Float, nullable=True)
    cambio: Mapped[float] = mapped_column(Float, nullable=True)
    forma_pago: Mapped[str] = mapped_column(
        String(50), default="Contado"
    )  # Contado, Transferencia, Tarjeta
    estado: Mapped[str] = mapped_column(
        String(50), default="Completada"
    )  # Pendiente, Completada, Cancelada
    notas: Mapped[str] = mapped_column(Text, nullable=True)

    # Relaciones
    detalles = relationship("DetalleVenta", back_populates="venta", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Venta(id={self.id}, numero_factura={self.numero_factura}, total={self.total})>"


class DetalleVenta(Base):
    """Modelo de detalle de venta"""

    __tablename__ = "detalles_venta"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    venta_id: Mapped[int] = mapped_column(ForeignKey("ventas.id"), index=True)
    producto_id: Mapped[int] = mapped_column(ForeignKey("productos.id"), index=True)
    cantidad: Mapped[int] = mapped_column(default=1)
    precio_unitario: Mapped[float] = mapped_column(Float)
    descuento_producto: Mapped[float] = mapped_column(Float, default=0)
    subtotal: Mapped[float] = mapped_column(Float)

    # Relaciones
    venta = relationship("Venta", back_populates="detalles")

    def __repr__(self) -> str:
        return f"<DetalleVenta(venta_id={self.venta_id}, producto_id={self.producto_id}, cantidad={self.cantidad})>"
