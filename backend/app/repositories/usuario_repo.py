"""Repository de Usuario"""

from typing import Optional

from sqlalchemy.orm import Session

from app.models.usuario import Usuario
from app.repositories.base import BaseRepository


class UsuarioRepository(BaseRepository[Usuario]):
    """Repository para operaciones de Usuario"""

    def __init__(self, session: Session):
        super().__init__(session, Usuario)

    def get_by_email(self, email: str) -> Optional[Usuario]:
        """Obtener usuario por email"""
        return self.session.query(Usuario).filter(Usuario.email == email).first()

    def get_activos(self, skip: int = 0, limit: int = 100) -> list[Usuario]:
        """Obtener solo usuarios activos"""
        return (
            self.session.query(Usuario)
            .filter(Usuario.activo == True)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_por_rol(self, rol: str, skip: int = 0, limit: int = 100) -> list[Usuario]:
        """Obtener usuarios por rol"""
        return (
            self.session.query(Usuario)
            .filter(Usuario.rol == rol, Usuario.activo == True)
            .offset(skip)
            .limit(limit)
            .all()
        )
