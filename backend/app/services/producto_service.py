"""ProductoService - Lógica de negocio de productos"""

from typing import List

from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundException, ConflictException, BadRequestException
from app.core.logging import log_user_action
from app.models.producto import Producto
from app.models.inventario import Inventario
from app.repositories.producto_repo import ProductoRepository
from app.repositories.inventario_repo import InventarioRepository
from app.schemas.producto import ProductoCreate, ProductoUpdate


class ProductoService:
    """Servicio de gestión de productos"""

    def __init__(self, db: Session, user_id: int):
        self.db = db
        self.user_id = user_id
        self.producto_repo = ProductoRepository(db)
        self.inventario_repo = InventarioRepository(db)

    def crear_producto(self, producto_data: ProductoCreate) -> Producto:
        """Crear un nuevo producto"""
        # Verificar si el código ya existe
        producto_existente = self.producto_repo.get_por_codigo(producto_data.codigo)
        if producto_existente:
            raise ConflictException("El código de producto ya está registrado")

        # Crear producto
        producto = self.producto_repo.create(producto_data.model_dump())

        # Crear registro de inventario
        self.inventario_repo.create(
            {"producto_id": producto.id, "cantidad": 0, "cantidad_minima": 10}
        )

        log_user_action(
            self.user_id,
            "Crear Producto",
            f"Producto creado: {producto.nombre} - ${producto.precio_venta} (ID: {producto.id})",
        )
        return producto

    def obtener_producto(self, producto_id: int) -> Producto:
        """Obtener producto por ID"""
        producto = self.producto_repo.get_by_id(producto_id)
        if not producto:
            raise NotFoundException("Producto", producto_id)
        return producto

    def obtener_por_codigo(self, codigo: str) -> Producto:
        """Obtener producto por código"""
        producto = self.producto_repo.get_por_codigo(codigo)
        if not producto:
            raise NotFoundException("Producto", f"código {codigo}")
        return producto

    def obtener_activos(self, skip: int = 0, limit: int = 100) -> List[Producto]:
        """Obtener solo productos activos"""
        return self.producto_repo.get_activos(skip, limit)

    def buscar_por_nombre(self, nombre: str, skip: int = 0, limit: int = 100) -> List[Producto]:
        """Buscar productos por nombre"""
        return self.producto_repo.buscar_por_nombre(nombre, skip, limit)

    def actualizar_producto(self, producto_id: int, producto_data: ProductoUpdate) -> Producto:
        """Actualizar un producto"""
        producto = self.obtener_producto(producto_id)

        # Validar precios
        if producto_data.precio_compra and producto_data.precio_venta:
            if producto_data.precio_compra >= producto_data.precio_venta:
                raise BadRequestException(
                    "El precio de venta debe ser mayor que el precio de compra"
                )

        producto_actualizado = self.producto_repo.update(
            producto_id, producto_data.model_dump(exclude_unset=True)
        )
        log_user_action(
            self.user_id,
            "Actualizar Producto",
            f"Producto actualizado: {producto.nombre} (ID: {producto_id})",
        )
        return producto_actualizado

    def actualizar_precio(self, producto_id: int, precio_venta: float) -> Producto:
        """Actualizar precio de venta de un producto"""
        producto = self.obtener_producto(producto_id)
        if producto.precio_compra and precio_venta <= producto.precio_compra:
            raise BadRequestException(
                "El precio de venta debe ser mayor que el precio de compra"
            )

        producto_actualizado = self.producto_repo.update(
            producto_id, {"precio_venta": precio_venta}
        )
        log_user_action(
            self.user_id,
            "Actualizar Precio",
            f"Precio actualizado: {producto.nombre} - ${precio_venta} (ID: {producto_id})",
        )
        return producto_actualizado

    def desactivar_producto(self, producto_id: int) -> Producto:
        """Desactivar un producto"""
        producto = self.obtener_producto(producto_id)
        producto_actualizado = self.producto_repo.update(producto_id, {"activo": False})
        log_user_action(
            self.user_id,
            "Desactivar Producto",
            f"Producto desactivado: {producto.nombre} (ID: {producto_id})",
        )
        return producto_actualizado
