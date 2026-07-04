"""Repository de Compra"""

from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.compra import Compra, DetalleCompra
from app.repositories.base import BaseRepository


class CompraRepository(BaseRepository[Compra]):
    """Repository para operaciones de Compra"""

    def __init__(self, session: Session):
        super().__init__(session, Compra)

    def get_por_numero(self, numero_compra: str) -> Optional[Compra]:
        """Obtener compra por número"""
        return (
            self.session.query(Compra)
            .filter(Compra.numero_compra == numero_compra)
            .first()
        )

    def get_por_proveedor(self, proveedor_id: int, skip: int = 0, limit: int = 100) -> list[Compra]:
        """Obtener compras de un proveedor"""
        return (
            self.session.query(Compra)
            .filter(Compra.proveedor_id == proveedor_id)
            .order_by(Compra.fecha_compra.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_del_periodo(self, fecha_inicio: datetime, fecha_fin: datetime, skip: int = 0, limit: int = 100) -> list[Compra]:
        """Obtener compras en un período"""
        return (
            self.session.query(Compra)
            .filter(Compra.fecha_compra >= fecha_inicio, Compra.fecha_compra <= fecha_fin)
            .order_by(Compra.fecha_compra.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_total_compras(self, fecha_inicio: datetime = None, fecha_fin: datetime = None) -> float:
        """Obtener total de compras en un período"""
        query = self.session.query(func.sum(Compra.total))
        if fecha_inicio:
            query = query.filter(Compra.fecha_compra >= fecha_inicio)
        if fecha_fin:
            query = query.filter(Compra.fecha_compra <= fecha_fin)
        result = query.scalar()
        return result or 0.0


class DetalleCompraRepository(BaseRepository[DetalleCompra]):
    """Repository para operaciones de DetalleCompra"""

    def __init__(self, session: Session):
        super().__init__(session, DetalleCompra)

    def get_por_compra(self, compra_id: int) -> list[DetalleCompra]:
        """Obtener detalles de una compra"""
        return self.session.query(DetalleCompra).filter(DetalleCompra.compra_id == compra_id).all()
