"""Endpoints de Clientes"""

from typing import List
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session

from app.api.v1.dependencies import get_current_user, get_gerente_user
from app.core.exceptions import AppException
from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.cliente import ClienteCreate, ClienteResponse, ClienteUpdate
from app.services.cliente_service import ClienteService

router = APIRouter(prefix="/clientes", tags=["Clientes"])


@router.post(
    "/",
    response_model=ClienteResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear nuevo cliente",
)
async def crear_cliente(
    cliente_data: ClienteCreate,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Crear un nuevo cliente"""
    try:
        service = ClienteService(db, current_user.id)
        cliente = service.crear_cliente(cliente_data)
        return cliente
    except AppException as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=e.status_code, detail=e.message)


@router.get(
    "/",
    response_model=List[ClienteResponse],
    summary="Listar todos los clientes",
)
async def listar_clientes(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Obtener lista de todos los clientes"""
    service = ClienteService(db, current_user.id)
    return service.obtener_todos(skip, limit)


@router.get(
    "/buscar",
    response_model=List[ClienteResponse],
    summary="Buscar clientes por nombre",
)
async def buscar_clientes(
    nombre: str = Query(..., min_length=1),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Buscar clientes por nombre"""
    service = ClienteService(db, current_user.id)
    return service.buscar_por_nombre(nombre, skip, limit)


@router.get(
    "/{cliente_id}",
    response_model=ClienteResponse,
    summary="Obtener cliente por ID",
)
async def obtener_cliente(
    cliente_id: int,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Obtener información de un cliente específico"""
    try:
        service = ClienteService(db, current_user.id)
        return service.obtener_cliente(cliente_id)
    except AppException as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=e.status_code, detail=e.message)


@router.put(
    "/{cliente_id}",
    response_model=ClienteResponse,
    summary="Actualizar cliente",
)
async def actualizar_cliente(
    cliente_id: int,
    cliente_data: ClienteUpdate,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Actualizar información de un cliente"""
    try:
        service = ClienteService(db, current_user.id)
        return service.actualizar_cliente(cliente_id, cliente_data)
    except AppException as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=e.status_code, detail=e.message)


@router.delete(
    "/{cliente_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar cliente",
)
async def eliminar_cliente(
    cliente_id: int,
    current_user: Usuario = Depends(get_gerente_user),
    db: Session = Depends(get_db),
):
    """Eliminar un cliente"""
    try:
        service = ClienteService(db, current_user.id)
        service.eliminar_cliente(cliente_id)
    except AppException as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=e.status_code, detail=e.message)
