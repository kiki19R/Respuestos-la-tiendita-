"""Repository de Cliente"""

from typing import Optional

from sqlalchemy.orm import Session

from app.models.cliente import Cliente
from app.repositories.base import BaseRepository


class ClienteRepository(BaseRepository[Cliente]):
    """Repository para operaciones de Cliente"""

    def __init__(self, session: Session):
        super().__init__(session, Cliente)

    def get_por_cedula(self, cedula: str) -> Optional[Cliente]:
        """Obtener cliente por cédula"""
        return self.session.query(Cliente).filter(Cliente.cedula == cedula).first()

    def get_por_email(self, email: str) -> Optional[Cliente]:
        """Obtener cliente por email"""
        return self.session.query(Cliente).filter(Cliente.email == email).first()

    def buscar_por_nombre(self, nombre: str, skip: int = 0, limit: int = 100) -> list[Cliente]:
        """Buscar clientes por nombre (búsqueda parcial)"""
        return (
            self.session.query(Cliente)
            .filter(Cliente.nombre.ilike(f"%{nombre}%"))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_por_tipo(self, tipo: str, skip: int = 0, limit: int = 100) -> list[Cliente]:
        """Obtener clientes por tipo"""
        return (
            self.session.query(Cliente)
            .filter(Cliente.tipo == tipo)
            .offset(skip)
            .limit(limit)
            .all()
        )
