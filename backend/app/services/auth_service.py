"""AuthService - Lógica de autenticación y gestión de usuarios"""

from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from app.core.logging import log_user_action
from app.core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
)
from app.core.exceptions import (
    UnauthorizedException,
    ConflictException,
    BadRequestException,
)
from app.models.usuario import Usuario
from app.repositories.usuario_repo import UsuarioRepository
from app.schemas.usuario import UsuarioCreate, LoginRequest


class AuthService:
    """Servicio de autenticación"""

    def __init__(self, db: Session):
        self.db = db
        self.usuario_repo = UsuarioRepository(db)

    def registrar_usuario(self, usuario_data: UsuarioCreate) -> Usuario:
        """Registra un nuevo usuario"""
        # Verificar si el email ya existe
        usuario_existente = self.usuario_repo.get_by_email(usuario_data.email)
        if usuario_existente:
            raise ConflictException("El email ya está registrado")

        # Hashear contraseña
        contrasena_hash = hash_password(usuario_data.contrasena)

        # Crear usuario
        usuario_dict = usuario_data.model_dump()
        usuario_dict["contrasena_hash"] = contrasena_hash
        del usuario_dict["contrasena"]

        usuario = self.usuario_repo.create(usuario_dict)
        log_user_action(usuario.id, "Registro", f"Usuario registrado: {usuario.email}")
        return usuario

    def login(self, login_data: LoginRequest) -> dict:
        """Realiza login y retorna tokens"""
        # Verificar usuario existe
        usuario = self.usuario_repo.get_by_email(login_data.email)
        if not usuario:
            raise UnauthorizedException("Email o contraseña incorrectos")

        # Verificar contraseña
        if not verify_password(login_data.contrasena, usuario.contrasena_hash):
            raise UnauthorizedException("Email o contraseña incorrectos")

        # Verificar usuario activo
        if not usuario.activo:
            raise UnauthorizedException("Usuario inactivo")

        # Crear tokens
        token_data = {"sub": usuario.email, "user_id": usuario.id, "rol": usuario.rol}
        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token(token_data)

        log_user_action(usuario.id, "Login", f"Usuario {usuario.email} inició sesión")

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "usuario": usuario,
        }

    def obtener_usuario_actual(self, user_id: int) -> Usuario:
        """Obtiene el usuario actual por ID"""
        usuario = self.usuario_repo.get_by_id(user_id)
        if not usuario:
            raise UnauthorizedException("Usuario no encontrado")
        return usuario

    def cambiar_contrasena(self, user_id: int, contrasena_actual: str, contrasena_nueva: str) -> bool:
        """Cambia la contraseña del usuario"""
        usuario = self.usuario_repo.get_by_id(user_id)
        if not usuario:
            raise UnauthorizedException("Usuario no encontrado")

        # Verificar contraseña actual
        if not verify_password(contrasena_actual, usuario.contrasena_hash):
            raise BadRequestException("Contraseña actual incorrecta")

        # Actualizar contraseña
        nueva_hash = hash_password(contrasena_nueva)
        self.usuario_repo.update(user_id, {"contrasena_hash": nueva_hash})

        log_user_action(user_id, "Cambio de contraseña", f"Contraseña actualizada")
        return True
