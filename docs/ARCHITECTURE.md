# 🏗️ Arquitectura del Sistema

## Visión General

Respuestos La Tiendita es un sistema ERP moderno construido con una arquitectura de **microservicios monolítica** que puede escalar a microservicios verdaderos cuando sea necesario.

---

## Capas de la Aplicación

### 1. Capa de Presentación (Frontend)

**Tecnología**: React 18 + TypeScript + Tailwind CSS

```
┌─���───────────────────────────────────┐
│  Componentes UI                      │
│  - Pages (Login, Dashboard, etc.)   │
│  - Components (Button, Form, etc.)  │
│  - Layouts                          │
└────────────┬────────────────────────┘
             │
┌────────────▼────────────────────────┐
│  State Management (Zustand)         │
│  - Auth Store                       │
│  - Global State                     │
└────────────┬────────────────────────┘
             │
┌────────────▼────────────────────────┐
│  Services Layer                     │
│  - API Client (axios)               │
│  - Auth Service                     │
│  - Data Services                    │
└─────────────────────────────────────┘
```

### 2. Capa de API (Backend)

**Tecnología**: FastAPI + Python

```
┌────────────────────────────────────┐
│  Endpoints REST                     │
│  /api/v1/{recurso}                 │
├────────────────────────────────────┤
│  Middleware                        │
│  - CORS                            │
│  - Error Handler                   │
│  - Logging                         │
├────────────────────────────────────┤
│  Dependencies                      │
│  - JWT Authentication              │
│  - Role Authorization              │
└────────────┬───────────────────────┘
             │
┌────────────▼───────────────────────┐
│  Services (Lógica de Negocio)      │
│  - AuthService                     │
│  - ClienteService                  │
│  - ProductoService                 │
│  - InventarioService               │
│  - VentaService                    │
│  - CompraService                   │
└────────────┬───────────────────────┘
             │
┌────────────▼───────────────────────┐
│  Repositories (Acceso a Datos)     │
│  - BaseRepository<T>               │
│  - ClienteRepository               │
│  - ProductoRepository              │
└─────────────────────────────────────┘
```

### 3. Capa de Datos (Database)

**Tecnología**: PostgreSQL + SQLAlchemy ORM

```
┌────────────────────────────────────┐
│  SQLAlchemy Models                 │
│  - Usuario                         │
│  - Cliente                         │
│  - Producto                        │
│  - Inventario                      │
│  - Venta / DetalleVenta            │
│  - Compra / DetalleCompra          │
│  - MovimientoInventario            │
└────────────┬───────────────────────┘
             │
┌────────────▼───────────────────────┐
│  PostgreSQL Database               │
│  - Tablas normalizadas             │
│  - Índices optimizados             │
│  - Foreign Keys                    │
└────────────────────────────────────┘
```

---

## Diagrama de Componentes

```
┌──────────────┐
│   Frontend   │  React + TypeScript
│   (Port 3000)│  Vite, Tailwind CSS
└──────┬───────┘
       │ HTTP/REST (JSON)
       │
┌──────▼────────────────────────────┐
│         nginx/Reverse Proxy       │  CORS, SSL
└──────┬────────────────────────────┘
       │
┌──────▼────────────────────────────┐
│  API Gateway / FastAPI             │  Port 8000
│  - Rate Limiting                   │  JWT Auth
│  - Request/Response Validation     │  Error Handling
└──────┬────────────────────────────┘
       │
┌──────┴────────────────────────────┐
│  Application Services              │
│  - Auth Service                    │
│  - Business Logic                  │
│  - Data Validation                 │
└──────┬────────────────────────────┘
       │
┌──────▼────────────────────────────┐
│  Data Access Layer (Repositories)  │
│  - Query Building                  │
│  - Data Transformation             │
└──────┬────────────────────────────┘
       │
┌──────▼────────────────────────────┐
│  PostgreSQL Database               │  Port 5432
│  - Persistent Storage              │  ACID Compliant
│  - Relationships                   │  Backup/Recovery
└────────────────────────────────────┘

┌────────────────────────────────────┐
│  Cache Layer (Redis)               │  Port 6379
│  - Session Storage                 │  Optional
│  - Query Cache                     │
└────────────────────────────────────┘
```

---

## Flujo de Datos - Ejemplo: Crear Venta

```
1. Usuario hace click en "Nueva Venta" (Frontend)
   ↓
2. Frontend abre formulario (DashboardPage)
   ↓
3. Usuario completa y envía (FormField + Button)
   ↓
4. Validación Zod (schemas/venta)
   ↓
5. POST /api/v1/ventas (ApiClient)
   └─→ Headers: Authorization: Bearer <token>
   ↓
6. Backend recibe (endpoints/ventas.py)
   ├─ Valida JWT (get_current_user)
   ├─ Verifica permisos (get_gerente_user)
   ↓
7. VentaService (services/venta_service.py)
   ├─ Validaciones de negocio
   ├─ Calcula totales
   ├─ Llama a InventarioService
   └─ Registra movimientos
   ↓
8. VentaRepository (repositories/venta_repo.py)
   ├─ Crea registro de Venta
   ├─ Crea DetalleVenta
   ├─ Actualiza Inventario
   └─ Registra MovimientoInventario
   ↓
9. SQLAlchemy ORM
   ├─ Valida constrains
   ├─ Genera SQL
   ↓
10. PostgreSQL
    ├─ Inserta en tabla ventas
    ├─ Inserta en detalles_venta
    ├─ Actualiza inventario
    └─ Inserta movimientos
    ↓
11. Backend retorna JSON con venta creada
    ↓
12. React Query (TanStack Query)
    ├─ Actualiza cache
    ├─ Revalida queries relacionadas
    ↓
13. Frontend muestra confirmación
    ├─ Recarga lista de ventas
    ├─ Muestra alert "Venta creada"
```

---

## Patrones de Diseño Utilizados

### 1. Repository Pattern

Aislamiento de la lógica de acceso a datos

```python
# Services usan Repositories
class VentaService:
    def __init__(self, db: Session, user_id: int):
        self.venta_repo = VentaRepository(db)
    
    def crear_venta(self, data):
        venta = self.venta_repo.create(data)  # Repository
        return venta
```

### 2. Service Layer Pattern

Lógica de negocio centralizada

```python
# Endpoints delegan en Services
@app.post("/api/v1/ventas")
def crear_venta(data, current_user):
    service = VentaService(db, current_user.id)  # Service
    return service.crear_venta(data)
```

### 3. Dependency Injection

Flexibilidad y testabilidad

```python
# FastAPI inyecta dependencias
@app.get("/clientes")
def listar(current_user = Depends(get_current_user), 
           db = Depends(get_db)):
    pass
```

### 4. State Management Pattern (Frontend)

Zustand con persistencia

```typescript
// Store centralizado
export const useAuthStore = create<AuthStore>()()
  persist((set, get) => ({
    // state
    // actions
  }))
```

---

## Modelo de Datos (ER Diagram)

```
┌─────────────────┐
│     Usuario     │
├─────────────────┤
│ id (PK)         │
│ email (UNIQUE)  │
│ nombre_completo │
│ contrasena_hash │
│ rol             │
│ activo          │
│ fecha_creacion  │
└─────────────────┘
        │
        │ crea
        ▼
┌──────────────────┐
│     Cliente      │
├──────────────────┤
│ id (PK)          │
│ nombre           │
│ cedula (UNIQUE)  │
│ telefono         │
│ email            │
│ direccion        │
│ tipo             │
└──────────────────┘

┌──────────────────┐         ┌─────────────────┐
│   Proveedor      │         │    Producto     │
├──────────────────┤         ├─────────────────┤
│ id (PK)          │◄────────│ proveedor_id (FK)
│ nombre           │         │ codigo (UNIQUE) │
│ rif (UNIQUE)     │         │ nombre          │
│ telefono         │         │ precio_compra   │
│ email            │         │ precio_venta    │
│ contacto         │         │ activo          │
│ direccion        │         └────────┬────────┘
└──────────────────┘                 │
                                     │ tiene
                                     ▼
                            ┌──────────────────┐
                            │   Inventario     │
                            ├──────────────────┤
                            │ id (PK)          │
                            │ producto_id (FK) │
                            │ cantidad         │
                            │ cantidad_minima  │
                            │ ubicacion        │
                            └──────────────────┘

┌──────────────────┐         ┌──────────────────┐
│      Venta       │         │  DetalleVenta    │
├──────────────────┤         ├──────────────────┤
│ id (PK)          │─────────│ venta_id (FK)    │
│ numero_factura   │         │ producto_id (FK) │
│ cliente_id (FK)  │         │ cantidad         │
│ usuario_id (FK)  │         │ precio_unitario  │
│ fecha_venta      │         │ descuento        │
│ total            │         │ subtotal         │
│ estado           │         └──────────────────┘
└──────────────────┘

┌──────────────────┐         ┌──────────────────┐
│     Compra       │         │  DetalleCompra   │
├──────────────────┤         ├──────────────────┤
│ id (PK)          │─────────│ compra_id (FK)   │
│ numero_compra    │         │ producto_id (FK) │
│ proveedor_id (FK)│         │ cantidad         │
│ usuario_id (FK)  │         │ precio_unitario  │
│ fecha_compra     │         │ subtotal         │
│ total            │         └──────────────────┘
│ estado           │
└──────────────────┘

┌────────────────────────┐
│ MovimientoInventario    │
├────────────────────────┤
│ id (PK)                │
│ producto_id (FK)       │
│ usuario_id (FK)        │
│ tipo_movimiento        │
│ cantidad               │
│ razon                  │
│ fecha_movimiento       │
└────────────────────────┘
```

---

## Seguridad

### Autenticación
- JWT tokens (stateless)
- Refresh tokens para renovación
- Expiración configurable

### Autorización
- Roles basados en acceso (RBAC)
- Validación en endpoints
- Middleware de JWT

### Validación
- Pydantic schemas (backend)
- Zod schemas (frontend)
- Sanitización de entrada

### Almacenamiento Seguro
- Contraseñas hasheadas con Bcrypt
- Environment variables para secretos
- No guardar datos sensibles en logs

---

## Performance

### Backend
- Índices en columnas frecuentes
- Caché con Redis
- Paginación de resultados
- Lazy loading de relaciones

### Frontend
- Code splitting con Vite
- React Query para caching
- Lazy loading de componentes
- Compresión de assets

---

## Escalabilidad Futura

```
Actual (Monolítica):
Frontend ←→ Backend ←→ PostgreSQL

Futuro (Microservicios):
Frontend ←→ API Gateway
                ├─→ Auth Service
                ├─→ Cliente Service
                ├─→ Producto Service
                ├─→ Venta Service
                ├─→ Compra Service
                └─→ Reporte Service
                
Cada servicio con su BD (Data per Service)
```

---

## Referencias

- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [SOLID Principles](https://en.wikipedia.org/wiki/SOLID)
- [Microservices Pattern](https://microservices.io/patterns/index.html)
