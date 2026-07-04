"""ProveedorService - Lógica de negocio de proveedores"""

from typing import List, Optional

from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundException, ConflictException
from app.core.logging import log_user_action
from app.models.proveedor import Proveedor
from app.repositories.proveedor_repo import ProveedorRepository


class ProveedorService:
    """Servicio de gestión de proveedores"""

    def __init__(self, db: Session, user_id: int):
        self.db = db
        self.user_id = user_id
        self.proveedor_repo = ProveedorRepository(db)

    def crear_proveedor(self, proveedor_data: dict) -> Proveedor:
        """Crear un nuevo proveedor"""
        # Verificar si el RIF ya existe
        if proveedor_data.get("rif"):
            proveedor_existente = self.proveedor_repo.get_por_rif(proveedor_data["rif"])
            if proveedor_existente:
                raise ConflictException("El RIF ya está registrado")

        proveedor = self.proveedor_repo.create(proveedor_data)
        log_user_action(
            self.user_id,
            "Crear Proveedor",
            f"Proveedor creado: {proveedor.nombre} (ID: {proveedor.id})",
        )
        return proveedor

    def obtener_proveedor(self, proveedor_id: int) -> Proveedor:
        """Obtener proveedor por ID"""
        proveedor = self.proveedor_repo.get_by_id(proveedor_id)
        if not proveedor:
            raise NotFoundException("Proveedor", proveedor_id)
        return proveedor

    def obtener_activos(self, skip: int = 0, limit: int = 100) -> List[Proveedor]:
        """Obtener solo proveedores activos"""
        return self.proveedor_repo.get_activos(skip, limit)

    def buscar_por_nombre(self, nombre: str, skip: int = 0, limit: int = 100) -> List[Proveedor]:
        """Buscar proveedores por nombre"""
        return self.proveedor_repo.buscar_por_nombre(nombre, skip, limit)

    def actualizar_proveedor(self, proveedor_id: int, proveedor_data: dict) -> Proveedor:
        """Actualizar un proveedor"""
        proveedor = self.obtener_proveedor(proveedor_id)

        # Verificar RIF si se actualiza
        if proveedor_data.get("rif") and proveedor_data["rif"] != proveedor.rif:
            proveedor_existente = self.proveedor_repo.get_por_rif(proveedor_data["rif"])
            if proveedor_existente:
                raise ConflictException("El RIF ya está registrado")

        proveedor_actualizado = self.proveedor_repo.update(proveedor_id, proveedor_data)
        log_user_action(
            self.user_id,
            "Actualizar Proveedor",
            f"Proveedor actualizado: {proveedor.nombre} (ID: {proveedor_id})",
        )
        return proveedor_actualizado

    def desactivar_proveedor(self, proveedor_id: int) -> Proveedor:
        """Desactivar un proveedor"""
        proveedor = self.obtener_proveedor(proveedor_id)
        proveedor_actualizado = self.proveedor_repo.update(proveedor_id, {"activo": False})
        log_user_action(
            self.user_id,
            "Desactivar Proveedor",
            f"Proveedor desactivado: {proveedor.nombre} (ID: {proveedor_id})",
        )
        return proveedor_actualizado
