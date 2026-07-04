"""Repository de Inventario"""

from typing import Optional

from sqlalchemy.orm import Session

from app.models.inventario import Inventario
from app.repositories.base import BaseRepository


class InventarioRepository(BaseRepository[Inventario]):
    """Repository para operaciones de Inventario"""

    def __init__(self, session: Session):
        super().__init__(session, Inventario)

    def get_por_producto(self, producto_id: int) -> Optional[Inventario]:
        """Obtener inventario de un producto"""
        return (
            self.session.query(Inventario)
            .filter(Inventario.producto_id == producto_id)
            .first()
        )

    def get_stock_bajo(self, skip: int = 0, limit: int = 100) -> list[Inventario]:
        """Obtener productos con stock bajo"""
        return (
            self.session.query(Inventario)
            .filter(Inventario.cantidad <= Inventario.cantidad_minima)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_sin_stock(self, skip: int = 0, limit: int = 100) -> list[Inventario]:
        """Obtener productos sin stock"""
        return (
            self.session.query(Inventario)
            .filter(Inventario.cantidad == 0)
            .offset(skip)
            .limit(limit)
            .all()
        )
