"""Schemas de Cliente"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class ClienteBase(BaseModel):
    """Schema base de cliente"""

    nombre: str = Field(..., min_length=2, max_length=255)
    cedula: Optional[str] = Field(None, max_length=20)
    telefono: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    direccion: Optional[str] = None
    tipo: str = Field("Consumidor Final", pattern="^(Consumidor Final|Empresa)$")
    notas: Optional[str] = None


class ClienteCreate(ClienteBase):
    """Schema para crear cliente"""

    pass


class ClienteUpdate(BaseModel):
    """Schema para actualizar cliente"""

    nombre: Optional[str] = Field(None, min_length=2, max_length=255)
    telefono: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    direccion: Optional[str] = None
    tipo: Optional[str] = Field(None, pattern="^(Consumidor Final|Empresa)$")
    notas: Optional[str] = None


class ClienteResponse(ClienteBase):
    """Schema de respuesta de cliente"""

    id: int
    fecha_registro: datetime
    fecha_actualizacion: datetime

    class Config:
        from_attributes = True
