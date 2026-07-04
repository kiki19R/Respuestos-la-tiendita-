"""Repository de Movimiento de Inventario"""

from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from app.models.movimiento_inventario import MovimientoInventario
from app.repositories.base import BaseRepository


class MovimientoInventarioRepository(BaseRepository[MovimientoInventario]):
    """Repository para operaciones de MovimientoInventario (Auditoría)"""

    def __init__(self, session: Session):
        super().__init__(session, MovimientoInventario)

    def get_por_producto(self, producto_id: int, skip: int = 0, limit: int = 100) -> list[MovimientoInventario]:
        """Obtener movimientos de un producto"""
        return (
            self.session.query(MovimientoInventario)
            .filter(MovimientoInventario.producto_id == producto_id)
            .order_by(MovimientoInventario.fecha_movimiento.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_por_usuario(self, usuario_id: int, skip: int = 0, limit: int = 100) -> list[MovimientoInventario]:
        """Obtener movimientos de un usuario"""
        return (
            self.session.query(MovimientoInventario)
            .filter(MovimientoInventario.usuario_id == usuario_id)
            .order_by(MovimientoInventario.fecha_movimiento.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_por_tipo(self, tipo_movimiento: str, skip: int = 0, limit: int = 100) -> list[MovimientoInventario]:
        """Obtener movimientos por tipo"""
        return (
            self.session.query(MovimientoInventario)
            .filter(MovimientoInventario.tipo_movimiento == tipo_movimiento)
            .order_by(MovimientoInventario.fecha_movimiento.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_del_periodo(self, fecha_inicio: datetime, fecha_fin: datetime, skip: int = 0, limit: int = 100) -> list[MovimientoInventario]:
        """Obtener movimientos en un período"""
        return (
            self.session.query(MovimientoInventario)
            .filter(
                MovimientoInventario.fecha_movimiento >= fecha_inicio,
                MovimientoInventario.fecha_movimiento <= fecha_fin
            )
            .order_by(MovimientoInventario.fecha_movimiento.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
