"""Endpoints de Autenticación"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.v1.dependencies import get_current_user
from app.core.exceptions import AppException
from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.usuario import (
    LoginRequest,
    TokenResponse,
    UsuarioCreate,
    UsuarioResponse,
)
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post(
    "/registro",
    response_model=UsuarioResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar nuevo usuario",
)
async def registrar(usuario_data: UsuarioCreate, db: Session = Depends(get_db)):
    """Registrar un nuevo usuario en el sistema"""
    try:
        auth_service = AuthService(db)
        usuario = auth_service.registrar_usuario(usuario_data)
        return usuario
    except AppException as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=e.status_code, detail=e.message)


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Iniciar sesión",
)
async def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """Iniciar sesión y obtener tokens JWT"""
    try:
        auth_service = AuthService(db)
        resultado = auth_service.login(login_data)
        return resultado
    except AppException as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=e.status_code, detail=e.message)


@router.get(
    "/me",
    response_model=UsuarioResponse,
    summary="Obtener usuario actual",
)
async def obtener_usuario_actual(current_user: Usuario = Depends(get_current_user)):
    """Obtener información del usuario autenticado"""
    return current_user
