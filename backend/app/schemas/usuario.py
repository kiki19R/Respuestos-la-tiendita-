"""Schemas de Usuario"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UsuarioBase(BaseModel):
    """Schema base de usuario"""

    email: EmailStr
    nombre_completo: str = Field(..., min_length=3, max_length=255)
    rol: str = Field("vendedor", pattern="^(admin|gerente|vendedor)$")


class UsuarioCreate(UsuarioBase):
    """Schema para crear usuario"""

    contraseña: str = Field(..., min_length=8, max_length=255)


class UsuarioUpdate(BaseModel):
    """Schema para actualizar usuario"""

    nombre_completo: Optional[str] = Field(None, min_length=3, max_length=255)
    email: Optional[EmailStr] = None
    rol: Optional[str] = Field(None, pattern="^(admin|gerente|vendedor)$")
    activo: Optional[bool] = None


class UsuarioResponse(UsuarioBase):
    """Schema de respuesta de usuario"""

    id: int
    activo: bool
    fecha_creacion: datetime
    fecha_actualizacion: datetime

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    """Schema para login"""

    email: EmailStr
    contraseña: str


class TokenResponse(BaseModel):
    """Schema de respuesta de tokens"""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    usuario: UsuarioResponse
