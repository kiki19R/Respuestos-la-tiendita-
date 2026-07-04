"""Endpoints de Inventario"""

from typing import List
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session

from app.api.v1.dependencies import get_current_user, get_gerente_user
from app.core.exceptions import AppException
from app.database import get_db
from app.models.usuario import Usuario
from app.services.inventario_service import InventarioService

router = APIRouter(prefix="/inventario", tags=["Inventario"])


@router.get(
    "/",
    summary="Obtener inventario completo",
)
async def obtener_inventario(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Obtener inventario completo"""
    service = InventarioService(db, current_user.id)
    return service.obtener_todo(skip, limit)


@router.get(
    "/stock-bajo",
    summary="Obtener productos con stock bajo",
)
async def obtener_stock_bajo(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Obtener productos con stock bajo"""
    service = InventarioService(db, current_user.id)
    return service.obtener_stock_bajo(skip, limit)


@router.get(
    "/sin-stock",
    summary="Obtener productos sin stock",
)
async def obtener_sin_stock(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Obtener productos sin stock"""
    service = InventarioService(db, current_user.id)
    return service.obtener_sin_stock(skip, limit)


@router.get(
    "/valor-total",
    summary="Obtener valor total del inventario",
)
async def obtener_valor_total(
    current_user: Usuario = Depends(get_gerente_user),
    db: Session = Depends(get_db),
):
    """Obtener valor total del inventario en dinero"""
    service = InventarioService(db, current_user.id)
    valor = service.obtener_valor_total_inventario()
    return {"valor_total": valor}


@router.get(
    "/{producto_id}",
    summary="Obtener inventario de un producto",
)
async def obtener_inventario_producto(
    producto_id: int,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Obtener inventario de un producto específico"""
    try:
        service = InventarioService(db, current_user.id)
        return service.obtener_inventario_producto(producto_id)
    except AppException as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=e.status_code, detail=e.message)


@router.patch(
    "/{producto_id}/actualizar",
    status_code=status.HTTP_200_OK,
    summary="Actualizar cantidad en inventario",
)
async def actualizar_cantidad(
    producto_id: int,
    cantidad_nueva: int = Query(..., ge=0),
    razon: str = Query("Ajuste manual"),
    current_user: Usuario = Depends(get_gerente_user),
    db: Session = Depends(get_db),
):
    """Actualizar cantidad en inventario"""
    try:
        service = InventarioService(db, current_user.id)
        return service.actualizar_cantidad(producto_id, cantidad_nueva, razon)
    except AppException as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=e.status_code, detail=e.message)


@router.patch(
    "/{producto_id}/incrementar",
    status_code=status.HTTP_200_OK,
    summary="Incrementar stock",
)
async def incrementar_stock(
    producto_id: int,
    cantidad: int = Query(..., gt=0),
    razon: str = Query("Entrada"),
    current_user: Usuario = Depends(get_gerente_user),
    db: Session = Depends(get_db),
):
    """Incrementar stock de un producto"""
    try:
        service = InventarioService(db, current_user.id)
        return service.incrementar_stock(producto_id, cantidad, razon)
    except AppException as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=e.status_code, detail=e.message)


@router.patch(
    "/{producto_id}/decrementar",
    status_code=status.HTTP_200_OK,
    summary="Decrementar stock",
)
async def decrementar_stock(
    producto_id: int,
    cantidad: int = Query(..., gt=0),
    razon: str = Query("Salida"),
    current_user: Usuario = Depends(get_gerente_user),
    db: Session = Depends(get_db),
):
    """Decrementar stock de un producto"""
    try:
        service = InventarioService(db, current_user.id)
        return service.decrementar_stock(producto_id, cantidad, razon)
    except AppException as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=e.status_code, detail=e.message)
