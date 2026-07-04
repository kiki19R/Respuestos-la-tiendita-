"""ClienteService - Lógica de negocio de clientes"""

from typing import List, Optional

from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundException, ConflictException
from app.core.logging import log_user_action
from app.models.cliente import Cliente
from app.repositories.cliente_repo import ClienteRepository
from app.schemas.cliente import ClienteCreate, ClienteUpdate


class ClienteService:
    """Servicio de gestión de clientes"""

    def __init__(self, db: Session, user_id: int):
        self.db = db
        self.user_id = user_id
        self.cliente_repo = ClienteRepository(db)

    def crear_cliente(self, cliente_data: ClienteCreate) -> Cliente:
        """Crear un nuevo cliente"""
        # Verificar si la cédula ya existe
        if cliente_data.cedula:
            cliente_existente = self.cliente_repo.get_por_cedula(cliente_data.cedula)
            if cliente_existente:
                raise ConflictException("La cédula ya está registrada")

        cliente = self.cliente_repo.create(cliente_data.model_dump())
        log_user_action(
            self.user_id,
            "Crear Cliente",
            f"Cliente creado: {cliente.nombre} (ID: {cliente.id})",
        )
        return cliente

    def obtener_cliente(self, cliente_id: int) -> Cliente:
        """Obtener cliente por ID"""
        cliente = self.cliente_repo.get_by_id(cliente_id)
        if not cliente:
            raise NotFoundException("Cliente", cliente_id)
        return cliente

    def obtener_todos(self, skip: int = 0, limit: int = 100) -> List[Cliente]:
        """Obtener todos los clientes"""
        return self.cliente_repo.get_all(skip, limit)

    def buscar_por_nombre(self, nombre: str, skip: int = 0, limit: int = 100) -> List[Cliente]:
        """Buscar clientes por nombre"""
        return self.cliente_repo.buscar_por_nombre(nombre, skip, limit)

    def actualizar_cliente(self, cliente_id: int, cliente_data: ClienteUpdate) -> Cliente:
        """Actualizar un cliente"""
        cliente = self.obtener_cliente(cliente_id)

        # Verificar cédula si se actualiza
        if cliente_data.cedula and cliente_data.cedula != cliente.cedula:
            cliente_existente = self.cliente_repo.get_por_cedula(cliente_data.cedula)
            if cliente_existente:
                raise ConflictException("La cédula ya está registrada")

        cliente_actualizado = self.cliente_repo.update(
            cliente_id, cliente_data.model_dump(exclude_unset=True)
        )
        log_user_action(
            self.user_id,
            "Actualizar Cliente",
            f"Cliente actualizado: {cliente.nombre} (ID: {cliente_id})",
        )
        return cliente_actualizado

    def eliminar_cliente(self, cliente_id: int) -> bool:
        """Eliminar un cliente"""
        cliente = self.obtener_cliente(cliente_id)
        self.cliente_repo.delete(cliente_id)
        log_user_action(
            self.user_id,
            "Eliminar Cliente",
            f"Cliente eliminado: {cliente.nombre} (ID: {cliente_id})",
        )
        return True
