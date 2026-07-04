# 📋 Documentación de API - Respuestos La Tiendita

## Base URL

```
http://localhost:8000/api/v1
```

## Autenticación

Todas las rutas (excepto login y registro) requieren un token JWT en el header:

```
Authorization: Bearer <access_token>
```

---

## 🔐 Autenticación

### Registro de Usuario

```http
POST /auth/registro
Content-Type: application/json

{
  "email": "usuario@example.com",
  "nombre_completo": "Nombre del Usuario",
  "contrasena": "password123456",
  "rol": "vendedor"
}
```

**Respuesta (201 Created):**
```json
{
  "id": 1,
  "email": "usuario@example.com",
  "nombre_completo": "Nombre del Usuario",
  "rol": "vendedor",
  "activo": true,
  "fecha_creacion": "2024-01-01T12:00:00"
}
```

---

### Login

```http
POST /auth/login
Content-Type: application/json

{
  "email": "usuario@example.com",
  "contrasena": "password123456"
}
```

**Respuesta (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "usuario": {
    "id": 1,
    "email": "usuario@example.com",
    "nombre_completo": "Nombre del Usuario",
    "rol": "vendedor",
    "activo": true
  }
}
```

---

### Obtener Usuario Actual

```http
GET /auth/me
Authorization: Bearer <access_token>
```

**Respuesta (200 OK):**
```json
{
  "id": 1,
  "email": "usuario@example.com",
  "nombre_completo": "Nombre del Usuario",
  "rol": "vendedor",
  "activo": true,
  "fecha_creacion": "2024-01-01T12:00:00"
}
```

---

## 👥 Clientes

### Crear Cliente

```http
POST /clientes
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "nombre": "Juan Pérez",
  "cedula": "12345678",
  "telefono": "5353264910",
  "email": "juan@example.com",
  "direccion": "Calle Principal 123",
  "tipo": "Consumidor Final"
}
```

### Listar Clientes

```http
GET /clientes?skip=0&limit=100
Authorization: Bearer <access_token>
```

### Buscar Clientes

```http
GET /clientes/buscar?nombre=Juan&skip=0&limit=100
Authorization: Bearer <access_token>
```

### Obtener Cliente

```http
GET /clientes/{cliente_id}
Authorization: Bearer <access_token>
```

### Actualizar Cliente

```http
PUT /clientes/{cliente_id}
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "nombre": "Juan Pérez Updated",
  "telefono": "5353264911"
}
```

### Eliminar Cliente

```http
DELETE /clientes/{cliente_id}
Authorization: Bearer <access_token>
```

---

## 📦 Productos

### Crear Producto

```http
POST /productos
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "codigo": "PROD-001",
  "nombre": "Filtro de Aire",
  "descripcion": "Filtro de aire para motores",
  "precio_compra": 10.00,
  "precio_venta": 25.00,
  "proveedor_id": 1
}
```

### Listar Productos

```http
GET /productos?skip=0&limit=100
Authorization: Bearer <access_token>
```

### Buscar Productos

```http
GET /productos/buscar?nombre=Filtro&skip=0&limit=100
Authorization: Bearer <access_token>
```

### Obtener Producto por Código

```http
GET /productos/codigo/PROD-001
Authorization: Bearer <access_token>
```

### Obtener Producto

```http
GET /productos/{producto_id}
Authorization: Bearer <access_token>
```

### Actualizar Producto

```http
PUT /productos/{producto_id}
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "nombre": "Filtro de Aire Premium",
  "precio_venta": 30.00
}
```

### Actualizar Precio

```http
PATCH /productos/{producto_id}/precio?precio_venta=32.00
Authorization: Bearer <access_token>
```

---

## 📊 Inventario

### Obtener Inventario

```http
GET /inventario?skip=0&limit=100
Authorization: Bearer <access_token>
```

### Productos con Stock Bajo

```http
GET /inventario/stock-bajo?skip=0&limit=100
Authorization: Bearer <access_token>
```

### Productos sin Stock

```http
GET /inventario/sin-stock?skip=0&limit=100
Authorization: Bearer <access_token>
```

### Valor Total del Inventario

```http
GET /inventario/valor-total
Authorization: Bearer <access_token>
```

**Respuesta:**
```json
{
  "valor_total": 15234.50
}
```

### Obtener Inventario de Producto

```http
GET /inventario/{producto_id}
Authorization: Bearer <access_token>
```

### Actualizar Cantidad

```http
PATCH /inventario/{producto_id}/actualizar?cantidad_nueva=50&razon=Ajuste manual
Authorization: Bearer <access_token>
```

### Incrementar Stock

```http
PATCH /inventario/{producto_id}/incrementar?cantidad=20&razon=Compra
Authorization: Bearer <access_token>
```

### Decrementar Stock

```http
PATCH /inventario/{producto_id}/decrementar?cantidad=5&razon=Venta
Authorization: Bearer <access_token>
```

---

## 🏭 Proveedores

### Crear Proveedor

```http
POST /proveedores
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "nombre": "Proveedor ABC",
  "rif": "J-12345678-9",
  "telefono": "5353264910",
  "email": "proveedor@example.com",
  "contacto": "Carlos González",
  "direccion": "Avenida Principal 456"
}
```

### Listar Proveedores Activos

```http
GET /proveedores?skip=0&limit=100
Authorization: Bearer <access_token>
```

### Buscar Proveedores

```http
GET /proveedores/buscar?nombre=ABC&skip=0&limit=100
Authorization: Bearer <access_token>
```

### Obtener Proveedor

```http
GET /proveedores/{proveedor_id}
Authorization: Bearer <access_token>
```

### Actualizar Proveedor

```http
PUT /proveedores/{proveedor_id}
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "nombre": "Proveedor ABC Updated",
  "telefono": "5353264911"
}
```

---

## 📝 Códigos de Error

| Código | Descripción |
|--------|-------------|
| 200 | OK |
| 201 | Creado exitosamente |
| 204 | Sin contenido |
| 400 | Solicitud inválida |
| 401 | No autenticado |
| 403 | Acceso prohibido |
| 404 | No encontrado |
| 409 | Conflicto (recurso duplicado) |
| 422 | Error de validación |
| 500 | Error interno del servidor |

---

## 🧪 Pruebas

Acceder a la documentación interactiva de Swagger UI:

```
http://localhost:8000/api/docs
```

---

## 📞 Soporte

Para más información o reportar bugs, contactar al equipo de desarrollo.
