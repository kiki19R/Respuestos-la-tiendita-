"""Repository de Producto"""

from typing import Optional

from sqlalchemy.orm import Session

from app.models.producto import Producto
from app.repositories.base import BaseRepository


class ProductoRepository(BaseRepository[Producto]):
    """Repository para operaciones de Producto"""

    def __init__(self, session: Session):
        super().__init__(session, Producto)

    def get_por_codigo(self, codigo: str) -> Optional[Producto]:
        """Obtener producto por código"""
        return self.session.query(Producto).filter(Producto.codigo == codigo).first()

    def get_activos(self, skip: int = 0, limit: int = 100) -> list[Producto]:
        """Obtener solo productos activos"""
        return (
            self.session.query(Producto)
            .filter(Producto.activo == True)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_por_proveedor(self, proveedor_id: int, skip: int = 0, limit: int = 100) -> list[Producto]:
        """Obtener productos por proveedor"""
        return (
            self.session.query(Producto)
            .filter(Producto.proveedor_id == proveedor_id, Producto.activo == True)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def buscar_por_nombre(self, nombre: str, skip: int = 0, limit: int = 100) -> list[Producto]:
        """Buscar productos por nombre"""
        return (
            self.session.query(Producto)
            .filter(Producto.nombre.ilike(f"%{nombre}%"), Producto.activo == True)
            .offset(skip)
            .limit(limit)
            .all()
        )
