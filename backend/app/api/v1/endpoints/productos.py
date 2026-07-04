"""Endpoints de Productos"""

from typing import List
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session

from app.api.v1.dependencies import get_current_user, get_gerente_user
from app.core.exceptions import AppException
from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.producto import ProductoCreate, ProductoResponse, ProductoUpdate
from app.services.producto_service import ProductoService

router = APIRouter(prefix="/productos", tags=["Productos"])


@router.post(
    "/",
    response_model=ProductoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear nuevo producto",
)
async def crear_producto(
    producto_data: ProductoCreate,
    current_user: Usuario = Depends(get_gerente_user),
    db: Session = Depends(get_db),
):
    """Crear un nuevo producto"""
    try:
        service = ProductoService(db, current_user.id)
        producto = service.crear_producto(producto_data)
        return producto
    except AppException as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=e.status_code, detail=e.message)


@router.get(
    "/",
    response_model=List[ProductoResponse],
    summary="Listar todos los productos",
)
async def listar_productos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Obtener lista de todos los productos activos"""
    service = ProductoService(db, current_user.id)
    return service.obtener_activos(skip, limit)


@router.get(
    "/buscar",
    response_model=List[ProductoResponse],
    summary="Buscar productos por nombre",
)
async def buscar_productos(
    nombre: str = Query(..., min_length=1),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Buscar productos por nombre"""
    service = ProductoService(db, current_user.id)
    return service.buscar_por_nombre(nombre, skip, limit)


@router.get(
    "/codigo/{codigo}",
    response_model=ProductoResponse,
    summary="Obtener producto por código",
)
async def obtener_producto_por_codigo(
    codigo: str,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Obtener producto por código"""
    try:
        service = ProductoService(db, current_user.id)
        return service.obtener_por_codigo(codigo)
    except AppException as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=e.status_code, detail=e.message)


@router.get(
    "/{producto_id}",
    response_model=ProductoResponse,
    summary="Obtener producto por ID",
)
async def obtener_producto(
    producto_id: int,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Obtener información de un producto"""
    try:
        service = ProductoService(db, current_user.id)
        return service.obtener_producto(producto_id)
    except AppException as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=e.status_code, detail=e.message)


@router.put(
    "/{producto_id}",
    response_model=ProductoResponse,
    summary="Actualizar producto",
)
async def actualizar_producto(
    producto_id: int,
    producto_data: ProductoUpdate,
    current_user: Usuario = Depends(get_gerente_user),
    db: Session = Depends(get_db),
):
    """Actualizar información de un producto"""
    try:
        service = ProductoService(db, current_user.id)
        return service.actualizar_producto(producto_id, producto_data)
    except AppException as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=e.status_code, detail=e.message)


@router.patch(
    "/{producto_id}/precio",
    response_model=ProductoResponse,
    summary="Actualizar precio de venta",
)
async def actualizar_precio(
    producto_id: int,
    precio_venta: float = Query(..., gt=0),
    current_user: Usuario = Depends(get_gerente_user),
    db: Session = Depends(get_db),
):
    """Actualizar precio de venta de un producto"""
    try:
        service = ProductoService(db, current_user.id)
        return service.actualizar_precio(producto_id, precio_venta)
    except AppException as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=e.status_code, detail=e.message)
