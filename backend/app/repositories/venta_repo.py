"""Repository de Venta"""

from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.venta import Venta, DetalleVenta
from app.repositories.base import BaseRepository


class VentaRepository(BaseRepository[Venta]):
    """Repository para operaciones de Venta"""

    def __init__(self, session: Session):
        super().__init__(session, Venta)

    def get_por_numero_factura(self, numero_factura: str) -> Optional[Venta]:
        """Obtener venta por número de factura"""
        return (
            self.session.query(Venta)
            .filter(Venta.numero_factura == numero_factura)
            .first()
        )

    def get_por_cliente(self, cliente_id: int, skip: int = 0, limit: int = 100) -> list[Venta]:
        """Obtener ventas de un cliente"""
        return (
            self.session.query(Venta)
            .filter(Venta.cliente_id == cliente_id)
            .order_by(Venta.fecha_venta.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_del_periodo(self, fecha_inicio: datetime, fecha_fin: datetime, skip: int = 0, limit: int = 100) -> list[Venta]:
        """Obtener ventas en un período"""
        return (
            self.session.query(Venta)
            .filter(Venta.fecha_venta >= fecha_inicio, Venta.fecha_venta <= fecha_fin)
            .order_by(Venta.fecha_venta.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_del_mes(self, skip: int = 0, limit: int = 100) -> list[Venta]:
        """Obtener ventas del mes actual"""
        ahora = datetime.utcnow()
        inicio_mes = ahora.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        return self.get_del_periodo(inicio_mes, ahora, skip, limit)

    def get_total_ventas(self, fecha_inicio: datetime = None, fecha_fin: datetime = None) -> float:
        """Obtener total de ventas en un período"""
        query = self.session.query(func.sum(Venta.total))
        if fecha_inicio:
            query = query.filter(Venta.fecha_venta >= fecha_inicio)
        if fecha_fin:
            query = query.filter(Venta.fecha_venta <= fecha_fin)
        result = query.scalar()
        return result or 0.0


class DetalleVentaRepository(BaseRepository[DetalleVenta]):
    """Repository para operaciones de DetalleVenta"""

    def __init__(self, session: Session):
        super().__init__(session, DetalleVenta)

    def get_por_venta(self, venta_id: int) -> list[DetalleVenta]:
        """Obtener detalles de una venta"""
        return self.session.query(DetalleVenta).filter(DetalleVenta.venta_id == venta_id).all()
