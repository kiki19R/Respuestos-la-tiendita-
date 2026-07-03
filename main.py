"""
Interfaz de línea de comandos (CLI) para el sistema de gestión de tienda
Proporciona menús interactivos para todas las operaciones
"""

from database import (
    BaseDatos, GestorClientes, GestorProveedores, GestorProductos,
    GestorInventario, GestorVentas, GestorCompras, inicializar_sistema
)
from invoice_generator import FacturaGenerator
from datetime import datetime
import os

class MenuPrincipal:
    """Menú principal del sistema"""
    
    def __init__(self):
        self.gestor_clientes = GestorClientes()
        self.gestor_proveedores = GestorProveedores()
        self.gestor_productos = GestorProductos()
        self.gestor_inventario = GestorInventario()
        self.gestor_ventas = GestorVentas()
        self.gestor_compras = GestorCompras()
    
    def limpiar_pantalla(self):
        """Limpia la pantalla"""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def pausa(self):
        """Pausa y espera entrada"""
        input("\n➤ Presiona ENTER para continuar...")
    
    def mostrar_encabezado(self, titulo):
        """Muestra un encabezado formateado"""
        print("\n" + "="*60)
        print(f"  🚗 {titulo}".center(60))
        print("="*60 + "\n")
    
    def menu_principal(self):
        """Muestra el menú principal"""
        while True:
            self.limpiar_pantalla()
            self.mostrar_encabezado("RESPUESTOS LA TIENDITA - SISTEMA DE GESTIÓN")
            
            print("""
            1️⃣  GESTIÓN DE CLIENTES
            2️⃣  GESTIÓN DE PROVEEDORES
            3️⃣  GESTIÓN DE PRODUCTOS
            4️⃣  GESTIÓN DE INVENTARIO
            5️⃣  REALIZAR VENTA (Generar Factura)
            6️⃣  REALIZAR COMPRA
            7️⃣  REPORTES Y ESTADÍSTICAS
            8️⃣  SALIR
            """)
            
            opcion = input("➤ Selecciona una opción (1-8): ").strip()
            
            if opcion == "1":
                self.menu_clientes()
            elif opcion == "2":
                self.menu_proveedores()
            elif opcion == "3":
                self.menu_productos()
            elif opcion == "4":
                self.menu_inventario()
            elif opcion == "5":
                self.menu_ventas()
            elif opcion == "6":
                self.menu_compras()
            elif opcion == "7":
                self.menu_reportes()
            elif opcion == "8":
                print("\n✅ ¡Hasta pronto! Respuestos La Tiendita\n")
                break
            else:
                print("❌ Opción no válida")
                self.pausa()
    
    def menu_clientes(self):
        """Menú de gestión de clientes"""
        while True:
            self.limpiar_pantalla()
            self.mostrar_encabezado("GESTIÓN DE CLIENTES")
            
            print("""
            1️⃣  AGREGAR CLIENTE
            2️⃣  VER TODOS LOS CLIENTES
            3️⃣  VOLVER AL MENÚ PRINCIPAL
            """)
            
            opcion = input("➤ Opción (1-3): ").strip()
            
            if opcion == "1":
                self.limpiar_pantalla()
                print("\n📝 NUEVO CLIENTE\n")
                nombre = input("Nombre: ").strip()
                cedula = input("Cédula (opcional): ").strip() or None
                telefono = input("Teléfono (opcional): ").strip() or None
                email = input("Email (opcional): ").strip() or None
                direccion = input("Dirección (opcional): ").strip() or None
                
                self.gestor_clientes.agregar(nombre, cedula, telefono, email, direccion)
                self.pausa()
            
            elif opcion == "2":
                self.limpiar_pantalla()
                print("\n📋 LISTA DE CLIENTES\n")
                clientes = self.gestor_clientes.obtener_todos()
                
                if clientes:
                    print(f"{'ID':<5} {'NOMBRE':<25} {'TELÉFONO':<12} {'EMAIL':<30}")
                    print("-" * 75)
                    for cliente in clientes:
                        print(f"{cliente['id']:<5} {cliente['nombre']:<25} {cliente['telefono'] or '-':<12} {cliente['email'] or '-':<30}")
                else:
                    print("❌ No hay clientes registrados")
                
                self.pausa()
            
            elif opcion == "3":
                break
            else:
                print("❌ Opción no válida")
                self.pausa()
    
    def menu_proveedores(self):
        """Menú de gestión de proveedores"""
        while True:
            self.limpiar_pantalla()
            self.mostrar_encabezado("GESTIÓN DE PROVEEDORES")
            
            print("""
            1️⃣  AGREGAR PROVEEDOR
            2️⃣  VER TODOS LOS PROVEEDORES
            3️⃣  VOLVER AL MENÚ PRINCIPAL
            """)
            
            opcion = input("➤ Opción (1-3): ").strip()
            
            if opcion == "1":
                self.limpiar_pantalla()
                print("\n📝 NUEVO PROVEEDOR\n")
                nombre = input("Nombre: ").strip()
                rif = input("RIF (opcional): ").strip() or None
                telefono = input("Teléfono (opcional): ").strip() or None
                email = input("Email (opcional): ").strip() or None
                contacto = input("Contacto (opcional): ").strip() or None
                direccion = input("Dirección (opcional): ").strip() or None
                
                self.gestor_proveedores.agregar(nombre, rif, telefono, email, contacto, direccion)
                self.pausa()
            
            elif opcion == "2":
                self.limpiar_pantalla()
                print("\n📋 LISTA DE PROVEEDORES\n")
                proveedores = self.gestor_proveedores.obtener_todos()
                
                if proveedores:
                    print(f"{'ID':<5} {'NOMBRE':<25} {'RIF':<15} {'TELÉFONO':<12}")
                    print("-" * 60)
                    for prov in proveedores:
                        print(f"{prov['id']:<5} {prov['nombre']:<25} {prov['rif'] or '-':<15} {prov['telefono'] or '-':<12}")
                else:
                    print("❌ No hay proveedores registrados")
                
                self.pausa()
            
            elif opcion == "3":
                break
            else:
                print("❌ Opción no válida")
                self.pausa()
    
    def menu_productos(self):
        """Menú de gestión de productos"""
        while True:
            self.limpiar_pantalla()
            self.mostrar_encabezado("GESTIÓN DE PRODUCTOS")
            
            print("""
            1️⃣  AGREGAR PRODUCTO
            2️⃣  VER TODOS LOS PRODUCTOS
            3️⃣  ACTUALIZAR PRECIO
            4️⃣  VOLVER AL MENÚ PRINCIPAL
            """)
            
            opcion = input("➤ Opción (1-4): ").strip()
            
            if opcion == "1":
                self.limpiar_pantalla()
                print("\n📝 NUEVO PRODUCTO\n")
                codigo = input("Código del producto: ").strip()
                nombre = input("Nombre: ").strip()
                descripcion = input("Descripción (opcional): ").strip() or None
                precio_compra = input("Precio de compra (USD, opcional): ").strip()
                precio_venta = input("Precio de venta (USD): ").strip()
                
                try:
                    precio_compra = float(precio_compra) if precio_compra else None
                    precio_venta = float(precio_venta)
                    
                    self.gestor_productos.agregar(codigo, nombre, descripcion, precio_compra, precio_venta)
                    self.pausa()
                except ValueError:
                    print("❌ Error: Los precios deben ser números válidos")
                    self.pausa()
            
            elif opcion == "2":
                self.limpiar_pantalla()
                print("\n📋 LISTA DE PRODUCTOS\n")
                productos = self.gestor_productos.obtener_todos()
                
                if productos:
                    print(f"{'ID':<5} {'CÓDIGO':<10} {'NOMBRE':<20} {'PRECIO':<10} {'CANT.':<6}")
                    print("-" * 60)
                    for prod in productos:
                        print(f"{prod['id']:<5} {prod['codigo']:<10} {prod['nombre']:<20} ${prod['precio_venta']:<9.2f} {prod['cantidad']:<6}")
                else:
                    print("❌ No hay productos registrados")
                
                self.pausa()
            
            elif opcion == "3":
                producto_id = input("\n📝 ID del producto: ").strip()
                try:
                    precio = float(input("Nuevo precio de venta: ").strip())
                    self.gestor_productos.actualizar_precio(int(producto_id), precio_venta=precio)
                    self.pausa()
                except ValueError:
                    print("❌ Error: Ingresa un valor numérico válido")
                    self.pausa()
            
            elif opcion == "4":
                break
            else:
                print("❌ Opción no válida")
                self.pausa()
    
    def menu_inventario(self):
        """Menú de gestión de inventario"""
        while True:
            self.limpiar_pantalla()
            self.mostrar_encabezado("GESTIÓN DE INVENTARIO")
            
            print("""
            1️⃣  VER INVENTARIO
            2️⃣  PRODUCTOS CON STOCK BAJO
            3️⃣  ACTUALIZAR CANTIDAD
            4️⃣  VALOR TOTAL DEL INVENTARIO
            5️⃣  VOLVER AL MENÚ PRINCIPAL
            """)
            
            opcion = input("➤ Opción (1-5): ").strip()
            
            if opcion == "1":
                self.limpiar_pantalla()
                print("\n📦 INVENTARIO ACTUAL\n")
                inventario = self.gestor_inventario.obtener_inventario()
                
                if inventario:
                    print(f"{'CÓDIGO':<10} {'PRODUCTO':<25} {'CANTIDAD':<8} {'MÍNIMO':<8} {'VALOR':<12}")
                    print("-" * 70)
                    for item in inventario:
                        valor = (item['cantidad'] * item['precio_compra']) if item['precio_compra'] else 0
                        print(f"{item['codigo']:<10} {item['nombre']:<25} {item['cantidad']:<8} {item['cantidad_minima']:<8} ${valor:<11.2f}")
                else:
                    print("❌ No hay productos en inventario")
                
                self.pausa()
            
            elif opcion == "2":
                self.limpiar_pantalla()
                print("\n⚠️  PRODUCTOS CON STOCK BAJO\n")
                productos = self.gestor_inventario.obtener_productos_bajos()
                
                if productos:
                    print(f"{'CÓDIGO':<10} {'PRODUCTO':<25} {'CANTIDAD':<8} {'MÍNIMO':<8}")
                    print("-" * 60)
                    for item in productos:
                        print(f"{item['codigo']:<10} {item['nombre']:<25} {item['cantidad']:<8} {item['cantidad_minima']:<8}")
                else:
                    print("✅ Todos los productos tienen stock suficiente")
                
                self.pausa()
            
            elif opcion == "3":
                producto_id = input("\n📝 ID del producto: ").strip()
                try:
                    cantidad = int(input("Nueva cantidad: ").strip())
                    razon = input("Razón del cambio (opcional): ").strip() or "Ajuste manual"
                    self.gestor_inventario.actualizar_cantidad(int(producto_id), cantidad, razon)
                    self.pausa()
                except ValueError:
                    print("❌ Error: Ingresa valores válidos")
                    self.pausa()
            
            elif opcion == "4":
                valor_total = self.gestor_inventario.obtener_valor_total()
                print(f"\n💰 Valor total del inventario: ${valor_total:.2f}")
                self.pausa()
            
            elif opcion == "5":
                break
            else:
                print("❌ Opción no válida")
                self.pausa()
    
    def menu_ventas(self):
        """Menú para realizar ventas"""
        self.limpiar_pantalla()
        self.mostrar_encabezado("NUEVA VENTA - GENERAR FACTURA")
        
        try:
            numero_factura = input("Número de factura: ").strip()
            factura = FacturaGenerator(numero_factura)
            
            print("\n📝 AGREGAR PRODUCTOS A LA FACTURA")
            print("(Ingresa 'listo' en el código para terminar)\n")
            
            while True:
                codigo = input("Código del producto (o 'listo'): ").strip()
                
                if codigo.lower() == 'listo':
                    break
                
                producto = self.gestor_productos.obtener_por_codigo(codigo)
                
                if producto:
                    print(f"\n✅ {producto['nombre']} - ${producto['precio_venta']:.2f}")
                    cantidad = int(input("Cantidad: "))
                    descuento = float(input("Descuento %: ") or "0")
                    
                    factura.agregar_producto(
                        codigo=producto['codigo'],
                        descripcion=producto['nombre'],
                        cantidad=cantidad,
                        precio_unitario=producto['precio_venta'],
                        descuento=descuento
                    )
                    print("✅ Producto agregado a la factura\n")
                else:
                    print("❌ Producto no encontrado\n")
            
            if factura.productos:
                print(f"\n💰 Subtotal: ${factura.subtotal:.2f}")
                pago = float(input("Monto de pago recibido: $"))
                factura.establecer_pago_recibido(pago)
                
                nombre_pdf = f"factura_{numero_factura}.pdf"
                factura.generar_factura(nombre_pdf)
                print(f"✅ Cambio: ${factura.calcular_cambio():.2f}")
            else:
                print("❌ No hay productos en la factura")
            
            self.pausa()
        
        except Exception as e:
            print(f"❌ Error: {e}")
            self.pausa()
    
    def menu_compras(self):
        """Menú para realizar compras"""
        self.limpiar_pantalla()
        self.mostrar_encabezado("NUEVA COMPRA A PROVEEDOR")
        
        try:
            numero_compra = input("Número de compra: ").strip()
            
            print("\n🏭 SELECCIONA UN PROVEEDOR:\n")
            proveedores = self.gestor_proveedores.obtener_todos()
            
            if not proveedores:
                print("❌ No hay proveedores registrados")
                self.pausa()
                return
            
            for idx, prov in enumerate(proveedores, 1):
                print(f"{idx}. {prov['nombre']}")
            
            opcion = int(input("\n➤ Opción: "))
            proveedor_id = proveedores[opcion - 1]['id']
            
            self.gestor_compras.crear_compra(numero_compra, proveedor_id)
            
            print("\n📝 AGREGAR PRODUCTOS A LA COMPRA")
            print("(Ingresa 'listo' para terminar)\n")
            
            compra = self.gestor_compras.db.obtener(
                "SELECT id FROM compras WHERE numero_compra = ?", (numero_compra,)
            )
            
            while True:
                codigo = input("Código del producto (o 'listo'): ").strip()
                
                if codigo.lower() == 'listo':
                    break
                
                producto = self.gestor_productos.obtener_por_codigo(codigo)
                
                if producto:
                    cantidad = int(input("Cantidad: "))
                    precio = float(input("Precio unitario: "))
                    
                    self.gestor_compras.agregar_detalle(compra['id'], producto['id'], cantidad, precio)
                    print("✅ Producto agregado\n")
                else:
                    print("❌ Producto no encontrado\n")
            
            self.gestor_compras.finalizar_compra(compra['id'])
            self.pausa()
        
        except Exception as e:
            print(f"❌ Error: {e}")
            self.pausa()
    
    def menu_reportes(self):
        """Menú de reportes y estadísticas"""
        while True:
            self.limpiar_pantalla()
            self.mostrar_encabezado("REPORTES Y ESTADÍSTICAS")
            
            print("""
            1️⃣  VENTAS DEL MES
            2️⃣  COMPRAS DEL MES
            3️⃣  PRODUCTOS CON STOCK BAJO
            4️⃣  VALOR TOTAL DEL INVENTARIO
            5️⃣  VOLVER AL MENÚ PRINCIPAL
            """)
            
            opcion = input("➤ Opción (1-5): ").strip()
            
            if opcion == "1":
                self.limpiar_pantalla()
                print("\n💰 VENTAS DEL MES\n")
                ventas = self.gestor_ventas.obtener_ventas(dias=30)
                
                if ventas:
                    total_ventas = sum(v['total'] for v in ventas if v['total'])
                    print(f"{'FACTURA':<15} {'FECHA':<15} {'CLIENTE':<20} {'TOTAL':<12}")
                    print("-" * 70)
                    for venta in ventas:
                        print(f"{venta['numero_factura']:<15} {venta['fecha_venta']:<15} {venta['cliente'] or 'N/A':<20} ${venta['total']:<11.2f}")
                    print("-" * 70)
                    print(f"{'TOTAL VENTAS':<50} ${total_ventas:.2f}")
                else:
                    print("❌ No hay ventas registradas este mes")
                
                self.pausa()
            
            elif opcion == "2":
                self.limpiar_pantalla()
                print("\n📦 COMPRAS DEL MES\n")
                compras = self.gestor_compras.obtener_compras(dias=30)
                
                if compras:
                    total_compras = sum(c['total'] for c in compras if c['total'])
                    print(f"{'COMPRA':<15} {'FECHA':<15} {'PROVEEDOR':<25} {'TOTAL':<12}")
                    print("-" * 75)
                    for compra in compras:
                        print(f"{compra['numero_compra']:<15} {compra['fecha_compra']:<15} {compra['proveedor'] or 'N/A':<25} ${compra['total']:<11.2f}")
                    print("-" * 75)
                    print(f"{'TOTAL COMPRAS':<55} ${total_compras:.2f}")
                else:
                    print("❌ No hay compras registradas este mes")
                
                self.pausa()
            
            elif opcion == "3":
                self.limpiar_pantalla()
                print("\n⚠️  PRODUCTOS CON STOCK BAJO\n")
                productos = self.gestor_inventario.obtener_productos_bajos()
                
                if productos:
                    print(f"{'CÓDIGO':<10} {'PRODUCTO':<30} {'STOCK':<8} {'MÍNIMO':<8}")
                    print("-" * 65)
                    for item in productos:
                        print(f"{item['codigo']:<10} {item['nombre']:<30} {item['cantidad']:<8} {item['cantidad_minima']:<8}")
                else:
                    print("✅ Todos los productos tienen stock suficiente")
                
                self.pausa()
            
            elif opcion == "4":
                valor_total = self.gestor_inventario.obtener_valor_total()
                print(f"\n💰 Valor total del inventario: ${valor_total:,.2f}")
                self.pausa()
            
            elif opcion == "5":
                break
            else:
                print("❌ Opción no válida")
                self.pausa()


def main():
    """Función principal"""
    inicializar_sistema()
    menu = MenuPrincipal()
    menu.menu_principal()


if __name__ == "__main__":
    main()