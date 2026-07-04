"""Repository de Proveedor"""

from typing import Optional

from sqlalchemy.orm import Session

from app.models.proveedor import Proveedor
from app.repositories.base import BaseRepository


class ProveedorRepository(BaseRepository[Proveedor]):
    """Repository para operaciones de Proveedor"""

    def __init__(self, session: Session):
        super().__init__(session, Proveedor)

    def get_por_rif(self, rif: str) -> Optional[Proveedor]:
        """Obtener proveedor por RIF"""
        return self.session.query(Proveedor).filter(Proveedor.rif == rif).first()

    def get_activos(self, skip: int = 0, limit: int = 100) -> list[Proveedor]:
        """Obtener solo proveedores activos"""
        return (
            self.session.query(Proveedor)
            .filter(Proveedor.activo == True)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def buscar_por_nombre(self, nombre: str, skip: int = 0, limit: int = 100) -> list[Proveedor]:
        """Buscar proveedores por nombre"""
        return (
            self.session.query(Proveedor)
            .filter(Proveedor.nombre.ilike(f"%{nombre}%"), Proveedor.activo == True)
            .offset(skip)
            .limit(limit)
            .all()
        )
