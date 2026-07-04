"""Modelo de Movimiento de Inventario"""

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class MovimientoInventario(Base):
    """Modelo para auditoría de movimientos de inventario"""

    __tablename__ = "movimientos_inventario"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    producto_id: Mapped[int] = mapped_column(ForeignKey("productos.id"), index=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), index=True)
    tipo_movimiento: Mapped[str] = mapped_column(
        String(50), index=True
    )  # Entrada, Salida, Ajuste, Venta, Compra
    cantidad: Mapped[int] = mapped_column(Integer)
    razon: Mapped[str] = mapped_column(Text, nullable=True)
    fecha_movimiento: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, index=True
    )

    def __repr__(self) -> str:
        return f"<MovimientoInventario(producto_id={self.producto_id}, tipo={self.tipo_movimiento}, cantidad={self.cantidad})>"
