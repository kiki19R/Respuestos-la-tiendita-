"""
Módulo de base de datos para el sistema de gestión de la tienda
Maneja: Productos, Inventario, Clientes, Proveedores, Ventas, Compras
"""

import sqlite3
from datetime import datetime
from pathlib import Path
from config import BASE_DATOS

class BaseDatos:
    """Gestor de base de datos SQLite"""
    
    def __init__(self, nombre_db=BASE_DATOS):
        self.nombre_db = nombre_db
        self.conexion = None
        self.inicializar()
    
    def conectar(self):
        """Conecta a la base de datos"""
        try:
            self.conexion = sqlite3.connect(self.nombre_db)
            self.conexion.row_factory = sqlite3.Row
            return self.conexion
        except sqlite3.Error as e:
            print(f"❌ Error de conexión: {e}")
            return None
    
    def desconectar(self):
        """Desconecta de la base de datos"""
        if self.conexion:
            self.conexion.close()
    
    def ejecutar(self, sql, parametros=None):
        """Ejecuta una consulta SQL"""
        try:
            cursor = self.conexion.cursor()
            if parametros:
                cursor.execute(sql, parametros)
            else:
                cursor.execute(sql)
            self.conexion.commit()
            return cursor
        except sqlite3.Error as e:
            print(f"❌ Error SQL: {e}")
            return None
    
    def obtener(self, sql, parametros=None):
        """Obtiene una fila de la base de datos"""
        try:
            cursor = self.conexion.cursor()
            if parametros:
                cursor.execute(sql, parametros)
            else:
                cursor.execute(sql)
            return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"❌ Error SQL: {e}")
            return None
    
    def obtener_todos(self, sql, parametros=None):
        """Obtiene todas las filas de una consulta"""
        try:
            cursor = self.conexion.cursor()
            if parametros:
                cursor.execute(sql, parametros)
            else:
                cursor.execute(sql)
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"❌ Error SQL: {e}")
            return []
    
    def inicializar(self):
        """Crea las tablas necesarias"""
        self.conectar()
        
        # Tabla de Clientes
        self.ejecutar("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            cedula TEXT UNIQUE,
            telefono TEXT,
            email TEXT,
            direccion TEXT,
            tipo TEXT DEFAULT 'Consumidor Final',
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # Tabla de Proveedores
        self.ejecutar("""
        CREATE TABLE IF NOT EXISTS proveedores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            rif TEXT UNIQUE,
            telefono TEXT,
            email TEXT,
            contacto TEXT,
            direccion TEXT,
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # Tabla de Productos
        self.ejecutar("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT UNIQUE NOT NULL,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            precio_compra REAL,
            precio_venta REAL NOT NULL,
            proveedor_id INTEGER,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (proveedor_id) REFERENCES proveedores(id)
        )
        """)
        
        # Tabla de Inventario
        self.ejecutar("""
        CREATE TABLE IF NOT EXISTS inventario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            producto_id INTEGER NOT NULL UNIQUE,
            cantidad INTEGER DEFAULT 0,
            cantidad_minima INTEGER DEFAULT 10,
            ubicacion TEXT,
            fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (producto_id) REFERENCES productos(id)
        )
        """)
        
        # Tabla de Compras
        self.ejecutar("""
        CREATE TABLE IF NOT EXISTS compras (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero_compra TEXT UNIQUE NOT NULL,
            proveedor_id INTEGER NOT NULL,
            fecha_compra TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            total REAL,
            estado TEXT DEFAULT 'Pendiente',
            notas TEXT,
            FOREIGN KEY (proveedor_id) REFERENCES proveedores(id)
        )
        """)
        
        # Tabla de Detalles de Compra
        self.ejecutar("""
        CREATE TABLE IF NOT EXISTS detalles_compra (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            compra_id INTEGER NOT NULL,
            producto_id INTEGER NOT NULL,
            cantidad INTEGER,
            precio_unitario REAL,
            subtotal REAL,
            FOREIGN KEY (compra_id) REFERENCES compras(id),
            FOREIGN KEY (producto_id) REFERENCES productos(id)
        )
        """)
        
        # Tabla de Ventas
        self.ejecutar("""
        CREATE TABLE IF NOT EXISTS ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero_factura TEXT UNIQUE NOT NULL,
            cliente_id INTEGER,
            fecha_venta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            subtotal REAL,
            descuento REAL DEFAULT 0,
            total REAL,
            pago_recibido REAL,
            cambio REAL,
            forma_pago TEXT DEFAULT 'Contado',
            estado TEXT DEFAULT 'Completada',
            FOREIGN KEY (cliente_id) REFERENCES clientes(id)
        )
        """)
        
        # Tabla de Detalles de Venta
        self.ejecutar("""
        CREATE TABLE IF NOT EXISTS detalles_venta (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            venta_id INTEGER NOT NULL,
            producto_id INTEGER NOT NULL,
            cantidad INTEGER,
            precio_unitario REAL,
            descuento_producto REAL DEFAULT 0,
            subtotal REAL,
            FOREIGN KEY (venta_id) REFERENCES ventas(id),
            FOREIGN KEY (producto_id) REFERENCES productos(id)
        )
        """)
        
        # Tabla de Movimientos de Inventario
        self.ejecutar("""
        CREATE TABLE IF NOT EXISTS movimientos_inventario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            producto_id INTEGER NOT NULL,
            tipo_movimiento TEXT,
            cantidad INTEGER,
            razon TEXT,
            fecha_movimiento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            usuario TEXT,
            FOREIGN KEY (producto_id) REFERENCES productos(id)
        )
        """)
        
        self.desconectar()
        print("✅ Base de datos inicializada correctamente")


class GestorClientes:
    """Gestor de clientes"""
    
    def __init__(self):
        self.db = BaseDatos()
        self.db.conectar()
    
    def agregar(self, nombre, cedula=None, telefono=None, email=None, direccion=None, tipo="Consumidor Final"):
        """Agrega un nuevo cliente"""
        try:
            self.db.ejecutar("""
            INSERT INTO clientes (nombre, cedula, telefono, email, direccion, tipo)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (nombre, cedula, telefono, email, direccion, tipo))
            print(f"✅ Cliente '{nombre}' agregado exitosamente")
            return True
        except Exception as e:
            print(f"❌ Error al agregar cliente: {e}")
            return False
    
    def obtener_todos(self):
        """Obtiene todos los clientes"""
        return self.db.obtener_todos("SELECT * FROM clientes ORDER BY nombre")
    
    def obtener_por_id(self, cliente_id):
        """Obtiene un cliente por ID"""
        return self.db.obtener("SELECT * FROM clientes WHERE id = ?", (cliente_id,))
    
    def actualizar(self, cliente_id, nombre=None, telefono=None, email=None, direccion=None):
        """Actualiza un cliente"""
        actualizaciones = []
        parametros = []
        
        if nombre: actualizaciones.append("nombre = ?"); parametros.append(nombre)
        if telefono: actualizaciones.append("telefono = ?"); parametros.append(telefono)
        if email: actualizaciones.append("email = ?"); parametros.append(email)
        if direccion: actualizaciones.append("direccion = ?"); parametros.append(direccion)
        
        parametros.append(cliente_id)
        
        if actualizaciones:
            sql = f"UPDATE clientes SET {', '.join(actualizaciones)} WHERE id = ?"
            self.db.ejecutar(sql, parametros)
            print("✅ Cliente actualizado")
            return True
        return False
    
    def eliminar(self, cliente_id):
        """Elimina un cliente"""
        self.db.ejecutar("DELETE FROM clientes WHERE id = ?", (cliente_id,))
        print("✅ Cliente eliminado")
        return True


class GestorProveedores:
    """Gestor de proveedores"""
    
    def __init__(self):
        self.db = BaseDatos()
        self.db.conectar()
    
    def agregar(self, nombre, rif=None, telefono=None, email=None, contacto=None, direccion=None):
        """Agrega un nuevo proveedor"""
        try:
            self.db.ejecutar("""
            INSERT INTO proveedores (nombre, rif, telefono, email, contacto, direccion)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (nombre, rif, telefono, email, contacto, direccion))
            print(f"✅ Proveedor '{nombre}' agregado exitosamente")
            return True
        except Exception as e:
            print(f"❌ Error al agregar proveedor: {e}")
            return False
    
    def obtener_todos(self):
        """Obtiene todos los proveedores"""
        return self.db.obtener_todos("SELECT * FROM proveedores ORDER BY nombre")
    
    def obtener_por_id(self, proveedor_id):
        """Obtiene un proveedor por ID"""
        return self.db.obtener("SELECT * FROM proveedores WHERE id = ?", (proveedor_id,))


class GestorProductos:
    """Gestor de productos"""
    
    def __init__(self):
        self.db = BaseDatos()
        self.db.conectar()
    
    def agregar(self, codigo, nombre, descripcion=None, precio_compra=None, precio_venta=None, proveedor_id=None):
        """Agrega un nuevo producto"""
        try:
            self.db.ejecutar("""
            INSERT INTO productos (codigo, nombre, descripcion, precio_compra, precio_venta, proveedor_id)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (codigo, nombre, descripcion, precio_compra, precio_venta, proveedor_id))
            
            # Obtener ID del producto insertado
            producto = self.db.obtener("SELECT id FROM productos WHERE codigo = ?", (codigo,))
            
            if producto:
                # Crear registro en inventario
                self.db.ejecutar("""
                INSERT INTO inventario (producto_id, cantidad, cantidad_minima)
                VALUES (?, ?, ?)
                """, (producto['id'], 0, 10))
                
                print(f"✅ Producto '{nombre}' agregado exitosamente")
                return True
        except Exception as e:
            print(f"❌ Error al agregar producto: {e}")
            return False
    
    def obtener_todos(self):
        """Obtiene todos los productos"""
        return self.db.obtener_todos("""
        SELECT p.*, i.cantidad, prov.nombre as proveedor
        FROM productos p
        LEFT JOIN inventario i ON p.id = i.producto_id
        LEFT JOIN proveedores prov ON p.proveedor_id = prov.id
        ORDER BY p.nombre
        """)
    
    def obtener_por_codigo(self, codigo):
        """Obtiene un producto por código"""
        return self.db.obtener("""
        SELECT p.*, i.cantidad
        FROM productos p
        LEFT JOIN inventario i ON p.id = i.producto_id
        WHERE p.codigo = ?
        """, (codigo,))
    
    def obtener_por_id(self, producto_id):
        """Obtiene un producto por ID"""
        return self.db.obtener("""
        SELECT p.*, i.cantidad
        FROM productos p
        LEFT JOIN inventario i ON p.id = i.producto_id
        WHERE p.id = ?
        """, (producto_id,))
    
    def actualizar_precio(self, producto_id, precio_venta=None, precio_compra=None):
        """Actualiza los precios de un producto"""
        try:
            if precio_venta is not None:
                self.db.ejecutar("UPDATE productos SET precio_venta = ? WHERE id = ?", 
                               (precio_venta, producto_id))
            if precio_compra is not None:
                self.db.ejecutar("UPDATE productos SET precio_compra = ? WHERE id = ?", 
                               (precio_compra, producto_id))
            print("✅ Precios actualizados")
            return True
        except Exception as e:
            print(f"❌ Error: {e}")
            return False


class GestorInventario:
    """Gestor de inventario"""
    
    def __init__(self):
        self.db = BaseDatos()
        self.db.conectar()
    
    def obtener_inventario(self):
        """Obtiene todo el inventario"""
        return self.db.obtener_todos("""
        SELECT i.*, p.codigo, p.nombre, p.precio_venta, p.precio_compra
        FROM inventario i
        JOIN productos p ON i.producto_id = p.id
        ORDER BY p.nombre
        """)
    
    def obtener_productos_bajos(self):
        """Obtiene productos con inventario bajo"""
        return self.db.obtener_todos("""
        SELECT i.*, p.codigo, p.nombre, p.precio_venta
        FROM inventario i
        JOIN productos p ON i.producto_id = p.id
        WHERE i.cantidad <= i.cantidad_minima
        ORDER BY i.cantidad
        """)
    
    def actualizar_cantidad(self, producto_id, cantidad, razon="Ajuste manual"):
        """Actualiza la cantidad de un producto"""
        try:
            # Obtener cantidad actual
            inv = self.db.obtener("SELECT cantidad FROM inventario WHERE producto_id = ?", (producto_id,))
            cantidad_anterior = inv['cantidad'] if inv else 0
            
            # Actualizar inventario
            self.db.ejecutar("""
            UPDATE inventario SET cantidad = ?, fecha_actualizacion = CURRENT_TIMESTAMP
            WHERE producto_id = ?
            """, (cantidad, producto_id))
            
            # Registrar movimiento
            cambio = cantidad - cantidad_anterior
            self.db.ejecutar("""
            INSERT INTO movimientos_inventario (producto_id, tipo_movimiento, cantidad, razon)
            VALUES (?, ?, ?, ?)
            """, (producto_id, 'Ajuste', cambio, razon))
            
            print(f"✅ Inventario actualizado (cambio: {cambio:+d})")
            return True
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def obtener_valor_total(self):
        """Calcula el valor total del inventario"""
        resultado = self.db.obtener("""
        SELECT SUM(i.cantidad * p.precio_compra) as valor_total
        FROM inventario i
        JOIN productos p ON i.producto_id = p.id
        WHERE p.precio_compra IS NOT NULL
        """)
        return resultado['valor_total'] if resultado['valor_total'] else 0


class GestorVentas:
    """Gestor de ventas"""
    
    def __init__(self):
        self.db = BaseDatos()
        self.db.conectar()
    
    def crear_venta(self, numero_factura, cliente_id=None, forma_pago="Contado"):
        """Crea una nueva venta"""
        try:
            self.db.ejecutar("""
            INSERT INTO ventas (numero_factura, cliente_id, forma_pago, estado)
            VALUES (?, ?, ?, 'Pendiente')
            """, (numero_factura, cliente_id, forma_pago))
            print(f"✅ Venta {numero_factura} creada")
            return True
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def agregar_detalle(self, venta_id, producto_id, cantidad, precio_unitario, descuento=0):
        """Agrega un detalle a la venta"""
        try:
            subtotal = cantidad * precio_unitario
            subtotal_con_descuento = subtotal - (subtotal * descuento / 100)
            
            self.db.ejecutar("""
            INSERT INTO detalles_venta 
            (venta_id, producto_id, cantidad, precio_unitario, descuento_producto, subtotal)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (venta_id, producto_id, cantidad, precio_unitario, descuento, subtotal_con_descuento))
            
            # Actualizar inventario
            inv = self.db.obtener("SELECT cantidad FROM inventario WHERE producto_id = ?", (producto_id,))
            if inv:
                nueva_cantidad = inv['cantidad'] - cantidad
                self.db.ejecutar("""
                UPDATE inventario SET cantidad = ? WHERE producto_id = ?
                """, (nueva_cantidad, producto_id))
                
                # Registrar movimiento
                self.db.ejecutar("""
                INSERT INTO movimientos_inventario (producto_id, tipo_movimiento, cantidad, razon)
                VALUES (?, ?, ?, ?)
                """, (producto_id, 'Venta', -cantidad, f'Venta #{venta_id}'))
            
            print(f"✅ Detalle agregado a venta")
            return True
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def finalizar_venta(self, venta_id, pago_recibido):
        """Finaliza una venta"""
        try:
            # Obtener totales
            detalles = self.db.obtener_todos("""
            SELECT SUM(subtotal) as total FROM detalles_venta WHERE venta_id = ?
            """, (venta_id,))
            
            total = detalles[0]['total'] if detalles and detalles[0]['total'] else 0
            cambio = pago_recibido - total
            
            self.db.ejecutar("""
            UPDATE ventas 
            SET subtotal = ?, total = ?, pago_recibido = ?, cambio = ?, estado = 'Completada'
            WHERE id = ?
            """, (total, total, pago_recibido, cambio, venta_id))
            
            print(f"✅ Venta finalizada - Cambio: ${cambio:.2f}")
            return True
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def obtener_ventas(self, dias=None):
        """Obtiene las ventas"""
        if dias:
            sql = f"""
            SELECT v.*, c.nombre as cliente
            FROM ventas v
            LEFT JOIN clientes c ON v.cliente_id = c.id
            WHERE DATE(v.fecha_venta) >= DATE('now', '-{dias} days')
            ORDER BY v.fecha_venta DESC
            """
        else:
            sql = """
            SELECT v.*, c.nombre as cliente
            FROM ventas v
            LEFT JOIN clientes c ON v.cliente_id = c.id
            ORDER BY v.fecha_venta DESC
            """
        return self.db.obtener_todos(sql)
    
    def obtener_total_ventas(self, dias=None):
        """Obtiene el total de ventas"""
        if dias:
            sql = f"""
            SELECT SUM(total) as total FROM ventas
            WHERE DATE(fecha_venta) >= DATE('now', '-{dias} days')
            """
        else:
            sql = "SELECT SUM(total) as total FROM ventas"
        
        resultado = self.db.obtener(sql)
        return resultado['total'] if resultado['total'] else 0


class GestorCompras:
    """Gestor de compras"""
    
    def __init__(self):
        self.db = BaseDatos()
        self.db.conectar()
    
    def crear_compra(self, numero_compra, proveedor_id, notas=None):
        """Crea una nueva compra"""
        try:
            self.db.ejecutar("""
            INSERT INTO compras (numero_compra, proveedor_id, estado, notas)
            VALUES (?, ?, 'Pendiente', ?)
            """, (numero_compra, proveedor_id, notas))
            print(f"✅ Compra {numero_compra} creada")
            return True
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def agregar_detalle(self, compra_id, producto_id, cantidad, precio_unitario):
        """Agrega un detalle a la compra"""
        try:
            subtotal = cantidad * precio_unitario
            
            self.db.ejecutar("""
            INSERT INTO detalles_compra (compra_id, producto_id, cantidad, precio_unitario, subtotal)
            VALUES (?, ?, ?, ?, ?)
            """, (compra_id, producto_id, cantidad, precio_unitario, subtotal))
            
            print(f"✅ Detalle agregado a compra")
            return True
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def finalizar_compra(self, compra_id):
        """Finaliza una compra y actualiza el inventario"""
        try:
            # Obtener detalles de compra
            detalles = self.db.obtener_todos("""
            SELECT * FROM detalles_compra WHERE compra_id = ?
            """, (compra_id,))
            
            total = 0
            for detalle in detalles:
                # Actualizar inventario
                inv = self.db.obtener("""
                SELECT cantidad FROM inventario WHERE producto_id = ?
                """, (detalle['producto_id'],))
                
                if inv:
                    nueva_cantidad = inv['cantidad'] + detalle['cantidad']
                    self.db.ejecutar("""
                    UPDATE inventario SET cantidad = ? WHERE producto_id = ?
                    """, (nueva_cantidad, detalle['producto_id']))
                    
                    # Registrar movimiento
                    self.db.ejecutar("""
                    INSERT INTO movimientos_inventario (producto_id, tipo_movimiento, cantidad, razon)
                    VALUES (?, ?, ?, ?)
                    """, (detalle['producto_id'], 'Compra', detalle['cantidad'], f'Compra #{compra_id}'))
                
                total += detalle['subtotal']
            
            # Actualizar estado de compra
            self.db.ejecutar("""
            UPDATE compras SET total = ?, estado = 'Completada' WHERE id = ?
            """, (total, compra_id))
            
            print(f"✅ Compra finalizada - Total: ${total:.2f}")
            return True
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def obtener_compras(self, dias=None):
        """Obtiene las compras"""
        if dias:
            sql = f"""
            SELECT c.*, p.nombre as proveedor
            FROM compras c
            LEFT JOIN proveedores p ON c.proveedor_id = p.id
            WHERE DATE(c.fecha_compra) >= DATE('now', '-{dias} days')
            ORDER BY c.fecha_compra DESC
            """
        else:
            sql = """
            SELECT c.*, p.nombre as proveedor
            FROM compras c
            LEFT JOIN proveedores p ON c.proveedor_id = p.id
            ORDER BY c.fecha_compra DESC
            """
        return self.db.obtener_todos(sql)


def inicializar_sistema():
    """Inicializa todo el sistema"""
    print("\n🔧 Inicializando sistema...")
    db = BaseDatos()
    print("✅ Sistema inicializado correctamente\n")