"""Endpoints de Proveedores"""

from typing import List
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session

from app.api.v1.dependencies import get_current_user, get_gerente_user
from app.core.exceptions import AppException
from app.database import get_db
from app.models.usuario import Usuario
from app.services.proveedor_service import ProveedorService

router = APIRouter(prefix="/proveedores", tags=["Proveedores"])


class ProveedorCreate(dict):
    pass


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Crear nuevo proveedor",
)
async def crear_proveedor(
    proveedor_data: dict,
    current_user: Usuario = Depends(get_gerente_user),
    db: Session = Depends(get_db),
):
    """Crear un nuevo proveedor"""
    try:
        service = ProveedorService(db, current_user.id)
        proveedor = service.crear_proveedor(proveedor_data)
        return proveedor
    except AppException as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=e.status_code, detail=e.message)


@router.get(
    "/",
    summary="Listar proveedores activos",
)
async def listar_proveedores(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Obtener lista de proveedores activos"""
    service = ProveedorService(db, current_user.id)
    return service.obtener_activos(skip, limit)


@router.get(
    "/buscar",
    summary="Buscar proveedores",
)
async def buscar_proveedores(
    nombre: str = Query(..., min_length=1),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Buscar proveedores por nombre"""
    service = ProveedorService(db, current_user.id)
    return service.buscar_por_nombre(nombre, skip, limit)


@router.get(
    "/{proveedor_id}",
    summary="Obtener proveedor",
)
async def obtener_proveedor(
    proveedor_id: int,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Obtener información de un proveedor"""
    try:
        service = ProveedorService(db, current_user.id)
        return service.obtener_proveedor(proveedor_id)
    except AppException as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=e.status_code, detail=e.message)


@router.put(
    "/{proveedor_id}",
    summary="Actualizar proveedor",
)
async def actualizar_proveedor(
    proveedor_id: int,
    proveedor_data: dict,
    current_user: Usuario = Depends(get_gerente_user),
    db: Session = Depends(get_db),
):
    """Actualizar información de un proveedor"""
    try:
        service = ProveedorService(db, current_user.id)
        return service.actualizar_proveedor(proveedor_id, proveedor_data)
    except AppException as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=e.status_code, detail=e.message)
