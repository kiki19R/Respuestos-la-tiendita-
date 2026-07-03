# 🚗 Sistema de Facturación y Gestión - Respuestos La Tiendita

Sistema completo de gestión para la tienda **Respuestos La Tiendita** con funcionalidades de:
- 📋 Inventario
- 💰 Ventas y Facturas
- 📦 Compras
- 👥 Gestión de Clientes
- 🏭 Gestión de Proveedores
- 📊 Reportes y Estadísticas

## ✨ Características Principales

✅ **Gestión de Productos**
- Registro de productos con código, nombre, precios
- Asociación con proveedores
- Actualización de precios

✅ **Control de Inventario**
- Seguimiento en tiempo real del stock
- Alertas de stock bajo
- Historial de movimientos
- Valor total del inventario

✅ **Gestión de Ventas**
- Generación de facturas en PDF profesionales
- Cálculo automático de totales y cambio
- Aplicación de descuentos por producto
- Registro de todas las ventas

✅ **Gestión de Compras**
- Registro de compras a proveedores
- Actualización automática de inventario
- Seguimiento de compras pendientes

✅ **Gestión de Clientes**
- Registro de información de clientes
- Historial de compras

✅ **Gestión de Proveedores**
- Base de datos de proveedores
- Contacto y detalles de proveedores

✅ **Reportes**
- Ventas del mes
- Compras del mes
- Productos con stock bajo
- Valor total del inventario

## 📋 Requisitos

- Python 3.7+
- SQLite3 (incluido en Python)
- Librerías adicionales (ver `requirements.txt`)

## 🚀 Instalación Rápida

```bash
# 1. Clonar el repositorio
git clone https://github.com/kiki19R/Respuestos-la-tiendita-.git
cd Respuestos-la-tiendita-

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar el sistema
python main.py
```

## 🎯 Uso

### Ejecutar el Sistema

```bash
python main.py
```

Esto abrirá un menú interactivo donde podrás:
- 1️⃣ Gestionar clientes
- 2️⃣ Gestionar proveedores
- 3️⃣ Crear y actualizar productos
- 4️⃣ Controlar inventario
- 5️⃣ Realizar ventas y generar facturas
- 6️⃣ Realizar compras
- 7️⃣ Ver reportes
- 8️⃣ Salir

## 📁 Estructura de Archivos

```
Responuestos-la-tiendita-/
├── main.py                    # CLI interactivo principal
├── database.py                # Módulo de base de datos
├── invoice_generator.py       # Generador de facturas PDF
├── config.py                  # Configuración del sistema
├── requirements.txt           # Dependencias Python
├── tienda_respuestos.db       # Base de datos (se crea automáticamente)
├── logo.png                   # Logo de la tienda (opcional)
└── README.md                  # Este archivo
```

## 💻 Ejemplo de Código

```python
from database import GestorProductos, GestorInventario

# Crear un producto
gestor = GestorProductos()
gestor.agregar(
    codigo="E787",
    nombre="Tdel volante superior",
    precio_venta=1.39
)

# Obtener inventario
gestor_inv = GestorInventario()
inventario = gestor_inv.obtener_inventario()
print(f"Valor total: ${gestor_inv.obtener_valor_total():.2f}")
```

## ⚙️ Configuración

Edita `config.py`:

```python
TIENDA = {
    'nombre': 'Respuestos La Tiendita',
    'rif': 'J-12345678-9',
    'telefono': '5353264910',
    'email': 'respuestoslatiendieta@gmail.com',
    'logo_path': 'logo.png'
}
```

## 🗄️ Base de Datos

SQLite con las siguientes tablas:
- **clientes** - Información de clientes
- **proveedores** - Información de proveedores
- **productos** - Catálogo de productos
- **inventario** - Stock y ubicación
- **ventas** - Registro de ventas
- **compras** - Registro de compras
- **movimientos_inventario** - Historial de cambios

## 📊 Funcionalidades

### Gestión de Productos
✅ Crear productos con código único
✅ Establecer precios de compra y venta
✅ Asociar con proveedores
✅ Actualizar precios dinámicamente

### Control de Inventario
✅ Registrar cantidad de stock
✅ Alertas de stock bajo
✅ Historial de movimientos
✅ Cálculo de valor total

### Ventas
✅ Crear facturas profesionales en PDF
✅ Aplicar descuentos por producto
✅ Calcular cambio automáticamente
✅ Actualizar inventario al vender
✅ Registrar cliente (opcional)

### Compras
✅ Registrar compras a proveedores
✅ Actualizar inventario automáticamente
✅ Calcular totales
✅ Historial de compras

### Reportes
✅ Ventas del mes
✅ Compras del mes
✅ Productos con stock bajo
✅ Valor total del inventario

## 🐛 Solución de Problemas

### Error: ModuleNotFoundError
```bash
pip install -r requirements.txt
```

### Base de datos bloqueada
```bash
rm tienda_respuestos.db
python main.py
```

### Las facturas no se generan
- Verifica permisos de escritura
- Instala reportlab: `pip install reportlab`

## 📝 Notas

- Las facturas se guardan como PDF en el directorio actual
- El inventario se actualiza automáticamente al realizar ventas
- Todos los precios están en USD
- La base de datos se crea automáticamente en la primera ejecución

## 📞 Soporte

Para reportar problemas, abre un **issue** en el repositorio.

## 📄 Licencia

Uso interno para Respuestos La Tiendita.

---

**Hecho con ❤️ para Respuestos La Tiendita**

**Última actualización**: Julio 2026