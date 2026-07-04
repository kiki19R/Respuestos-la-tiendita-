"""Dependencias para los endpoints"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from sqlalchemy.orm import Session

from app.config import get_settings
from app.core.security import decode_token
from app.database import get_db
from app.models.usuario import Usuario

security = HTTPBearer()
config = get_settings()


async def get_current_user(
    credentials: HTTPAuthCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> Usuario:
    """Obtiene el usuario actual del token JWT"""
    token = credentials.credentials
    payload = decode_token(token)
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id = payload.get("user_id")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    from app.repositories.usuario_repo import UsuarioRepository
    repo = UsuarioRepository(db)
    usuario = repo.get_by_id(user_id)
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not usuario.activo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo",
        )
    
    return usuario


async def get_admin_user(current_user: Usuario = Depends(get_current_user)) -> Usuario:
    """Verifica que el usuario sea administrador"""
    if current_user.rol != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requieren permisos de administrador",
        )
    return current_user


async def get_gerente_user(current_user: Usuario = Depends(get_current_user)) -> Usuario:
    """Verifica que el usuario sea gerente o administrador"""
    if current_user.rol not in ["admin", "gerente"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requieren permisos de gerente o administrador",
        )
    return current_user
