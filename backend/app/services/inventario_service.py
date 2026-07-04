"""InventarioService - Lógica de control de inventario"""

from typing import List
from datetime import datetime

from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundException, BadRequestException
from app.core.logging import log_user_action
from app.models.inventario import Inventario
from app.models.movimiento_inventario import MovimientoInventario
from app.repositories.inventario_repo import InventarioRepository
from app.repositories.movimiento_inventario_repo import MovimientoInventarioRepository


class InventarioService:
    """Servicio de gestión de inventario"""

    def __init__(self, db: Session, user_id: int):
        self.db = db
        self.user_id = user_id
        self.inventario_repo = InventarioRepository(db)
        self.movimiento_repo = MovimientoInventarioRepository(db)

    def obtener_inventario_producto(self, producto_id: int) -> Inventario:
        """Obtener inventario de un producto"""
        inventario = self.inventario_repo.get_por_producto(producto_id)
        if not inventario:
            raise NotFoundException("Inventario del producto", producto_id)
        return inventario

    def obtener_todo(self, skip: int = 0, limit: int = 100) -> List[Inventario]:
        """Obtener todo el inventario"""
        return self.inventario_repo.get_all(skip, limit)

    def obtener_stock_bajo(self, skip: int = 0, limit: int = 100) -> List[Inventario]:
        """Obtener productos con stock bajo"""
        return self.inventario_repo.get_stock_bajo(skip, limit)

    def obtener_sin_stock(self, skip: int = 0, limit: int = 100) -> List[Inventario]:
        """Obtener productos sin stock"""
        return self.inventario_repo.get_sin_stock(skip, limit)

    def actualizar_cantidad(
        self,
        producto_id: int,
        cantidad_nueva: int,
        razon: str = "Ajuste manual",
        tipo_movimiento: str = "Ajuste",
    ) -> Inventario:
        """Actualizar cantidad en inventario"""
        if cantidad_nueva < 0:
            raise BadRequestException("La cantidad no puede ser negativa")

        inventario = self.obtener_inventario_producto(producto_id)
        cantidad_anterior = inventario.cantidad
        cantidad_cambio = cantidad_nueva - cantidad_anterior

        # Actualizar inventario
        inventario_actualizado = self.inventario_repo.update(
            inventario.id, {"cantidad": cantidad_nueva}
        )

        # Registrar movimiento
        self.movimiento_repo.create(
            {
                "producto_id": producto_id,
                "usuario_id": self.user_id,
                "tipo_movimiento": tipo_movimiento,
                "cantidad": cantidad_cambio,
                "razon": razon,
            }
        )

        log_user_action(
            self.user_id,
            "Actualizar Inventario",
            f"Cantidad actualizada: Producto {producto_id} - {cantidad_anterior} → {cantidad_nueva} ({razon})",
        )
        return inventario_actualizado

    def incrementar_stock(self, producto_id: int, cantidad: int, razon: str = "Entrada") -> Inventario:
        """Incrementar stock de un producto"""
        inventario = self.obtener_inventario_producto(producto_id)
        nueva_cantidad = inventario.cantidad + cantidad
        return self.actualizar_cantidad(
            producto_id, nueva_cantidad, razon, "Entrada"
        )

    def decrementar_stock(
        self, producto_id: int, cantidad: int, razon: str = "Salida"
    ) -> Inventario:
        """Decrementar stock de un producto"""
        inventario = self.obtener_inventario_producto(producto_id)
        if inventario.cantidad < cantidad:
            raise BadRequestException(
                f"Stock insuficiente. Disponible: {inventario.cantidad}, Solicitado: {cantidad}"
            )
        nueva_cantidad = inventario.cantidad - cantidad
        return self.actualizar_cantidad(
            producto_id, nueva_cantidad, razon, "Salida"
        )

    def obtener_valor_total_inventario(self) -> float:
        """Calcular valor total del inventario"""
        inventarios = self.obtener_todo(limit=10000)
        total = 0.0
        for inv in inventarios:
            # Obtener el producto para el precio de compra
            if inv.producto_id:
                from app.repositories.producto_repo import ProductoRepository
                producto_repo = ProductoRepository(self.db)
                producto = producto_repo.get_by_id(inv.producto_id)
                if producto and producto.precio_compra:
                    total += inv.cantidad * producto.precio_compra
        return total
