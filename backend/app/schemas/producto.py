"""Schemas de Producto"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ProductoBase(BaseModel):
    """Schema base de producto"""

    codigo: str = Field(..., min_length=1, max_length=50)
    nombre: str = Field(..., min_length=2, max_length=255)
    descripcion: Optional[str] = None
    precio_compra: Optional[float] = Field(None, gt=0)
    precio_venta: float = Field(..., gt=0)
    proveedor_id: Optional[int] = None


class ProductoCreate(ProductoBase):
    """Schema para crear producto"""

    pass


class ProductoUpdate(BaseModel):
    """Schema para actualizar producto"""

    nombre: Optional[str] = Field(None, min_length=2, max_length=255)
    descripcion: Optional[str] = None
    precio_compra: Optional[float] = Field(None, gt=0)
    precio_venta: Optional[float] = Field(None, gt=0)
    proveedor_id: Optional[int] = None
    activo: Optional[bool] = None


class ProductoResponse(ProductoBase):
    """Schema de respuesta de producto"""

    id: int
    activo: bool
    cantidad_inventario: Optional[int] = None
    fecha_creacion: datetime
    fecha_actualizacion: datetime

    class Config:
        from_attributes = True
