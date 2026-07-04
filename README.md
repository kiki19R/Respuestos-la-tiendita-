# 🚗 Respuestos La Tiendita - Sistema ERP Profesional

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![React 18+](https://img.shields.io/badge/react-18+-61dafb.svg)](https://react.dev/)
[![PostgreSQL 16](https://img.shields.io/badge/postgresql-16-336791.svg)](https://www.postgresql.org/)

> Sistema ERP completo, profesional y escalable para la gestión de tiendas de repuestos.

## ✨ Características

### 🔐 Seguridad
- ✅ Autenticación JWT con tokens de acceso y refresco
- ✅ Contraseñas hasheadas con Bcrypt
- ✅ Control de roles (admin, gerente, vendedor)
- ✅ Rate limiting y validación de entrada
- ✅ Logging de auditoría completo

### 📊 Gestión de Inventario
- ✅ Control de stock en tiempo real
- ✅ Alertas de stock bajo
- ✅ Historial de movimientos de inventario
- ✅ Cálculo de valor total del inventario
- ✅ Búsqueda avanzada de productos

### 💰 Gestión de Ventas
- ✅ Facturación electrónica profesional
- ✅ Cálculo automático de totales y cambio
- ✅ Descuentos por producto
- ✅ Múltiples formas de pago
- ✅ Generación de PDF

### 📦 Gestión de Compras
- ✅ Registro de compras a proveedores
- ✅ Actualización automática de inventario
- ✅ Seguimiento de compras pendientes
- ✅ Historial completo de transacciones

### 👥 Gestión de Clientes y Proveedores
- ✅ Base de datos de clientes y proveedores
- ✅ Información de contacto detallada
- ✅ Historial de transacciones
- ✅ Búsqueda y filtrado

### 📈 Reportes y Estadísticas
- ✅ Ventas por período
- ✅ Compras por período
- ✅ Productos con stock bajo
- ✅ Valor total del inventario
- ✅ Gráficos interactivos

### 🎨 Interfaz Moderna
- ✅ Diseño responsive con Tailwind CSS
- ✅ Componentes reutilizables
- ✅ Validaciones en tiempo real
- ✅ Interfaz intuitiva y fácil de usar

---

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────────────┐
│                     FRONTEND (React)                     │
│  - TypeScript, Vite, Tailwind CSS                       │
│  - React Router, React Query, Zustand                   │
│  - Componentes reutilizables, Validaciones con Zod      │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ↓ HTTP/REST
┌─────────────────────────────────────────────────────────┐
│                   API REST (FastAPI)                     │
│  - Python 3.11, FastAPI, Uvicorn                        │
│  - JWT Authentication, CORS, Rate Limiting              │
│  - Endpoints: Auth, Clientes, Productos, Inventario     │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ↓ SQL
┌─────────────────────────────────────────────────────────┐
│                  DATABASE (PostgreSQL)                   │
│  - PostgreSQL 16, SQLAlchemy ORM                        │
│  - 10 tablas relacionadas, Índices optimizados          │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│              INFRASTRUCTURE (Docker)                     │
│  - Docker Compose con 6 servicios                       │
│  - Postgres, Backend, Frontend, pgAdmin, Redis          │
└─────────────────────────────────────────────────────────┘
```

---

## 🚀 Inicio Rápido

### Con Docker (Recomendado)

```bash
# 1. Clonar repositorio
git clone https://github.com/kiki19R/Respuestos-la-tiendita-.git
cd Respuestos-la-tiendita-

# 2. Configurar variables de entorno
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# 3. Iniciar servicios
docker-compose up -d

# 4. Crear usuario admin (ver SETUP.md para detalles)

# 5. Acceder
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# API Docs: http://localhost:8000/api/docs
```

### Localmente (Sin Docker)

Ver [SETUP.md](./SETUP.md) para instrucciones detalladas.

---

## 📁 Estructura del Proyecto

```
Responuestos-la-tiendita-/
├── backend/                          # FastAPI Backend
│   ├── app/
│   │   ├── api/                     # Endpoints REST
│   │   ├── core/                    # Seguridad, excepciones, logging
│   │   ├── models/                  # Modelos SQLAlchemy
│   │   ├── schemas/                 # Schemas Pydantic
│   │   ├── services/                # Lógica de negocio
│   │   ├── repositories/            # Acceso a datos
│   │   └── main.py                  # Aplicación principal
│   ├── tests/                       # Tests unitarios e integración
│   ├── requirements.txt             # Dependencias Python
│   ├── Dockerfile                   # Build backend
│   └── docker-compose.yml           # Orquestación de servicios
│
├── frontend/                         # React + TypeScript
│   ├── src/
│   │   ├── components/              # Componentes reutilizables
│   │   ├── pages/                   # Páginas
│   │   ├── services/                # Clientes API
│   │   ├── store/                   # Estado global (Zustand)
│   │   ├── schemas/                 # Validaciones (Zod)
│   │   ├── types/                   # Tipos TypeScript
│   │   └── App.tsx                  # Componente principal
│   ├── package.json                 # Dependencias Node
│   ├── vite.config.ts               # Configuración Vite
│   ├── tailwind.config.js           # Configuración Tailwind
│   ├── Dockerfile                   # Build frontend
│   └── .env.example                 # Variables de entorno
│
├── docker-compose.yml               # Orquestación completa
├── SETUP.md                         # Guía de instalación
├── README.md                        # Este archivo
└── docs/                            # Documentación adicional
```

---

## 🔑 Credenciales de Prueba

| Campo | Valor |
|-------|-------|
| Email | admin@example.com |
| Contraseña | admin123456 |
| Rol | admin |

**Nota:** Cambiar credenciales en producción.

---

## 📚 Documentación

- [Guía de Instalación](./SETUP.md)
- [Documentación de API](./docs/API.md) (próximamente)
- [Arquitectura del Sistema](./docs/ARCHITECTURE.md) (próximamente)
- [Guía de Deployment](./docs/DEPLOYMENT.md) (próximamente)

---

## 🛠️ Stack Tecnológico

### Backend
- **FastAPI** - Framework web moderno y rápido
- **SQLAlchemy** - ORM robusto para Python
- **PostgreSQL** - Base de datos confiable
- **Alembic** - Migraciones de BD
- **Pytest** - Testing

### Frontend
- **React 18** - Biblioteca UI
- **TypeScript** - Seguridad de tipos
- **Vite** - Build tool rápido
- **Tailwind CSS** - Estilos
- **React Query** - Manejo de datos
- **Zustand** - Estado global
- **React Hook Form** - Gestión de formularios
- **Zod** - Validaciones

### DevOps
- **Docker** - Containerización
- **Docker Compose** - Orquestación
- **PostgreSQL 16** - Base de datos
- **Redis** - Caching (opcional)

---

## 🌟 Características Futuras

- [ ] Integración con múltiples sucursales
- [ ] Punto de venta (POS) integrado
- [ ] App móvil nativa
- [ ] Integración con plataformas de pago
- [ ] Sistema de notificaciones por email/SMS
- [ ] Soporte multimoneda
- [ ] Análisis con IA/ML
- [ ] API pública para integraciones

---

## 🤝 Contribuir

Los pull requests son bienvenidos. Para cambios importantes, abre primero un issue para discutir los cambios propuestos.

---

## 📄 Licencia

Este proyecto está bajo licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

---

## 👨‍💻 Autor

**kiki19R** - [GitHub](https://github.com/kiki19R)

---

## 📞 Soporte

Para reportar bugs o solicitar features, abre un [GitHub Issue](https://github.com/kiki19R/Respuestos-la-tiendita-/issues).

---

## 🙏 Agradecimientos

Gracias a todos los que contribuyen al desarrollo de este proyecto.

---

**Hecho con ❤️ para Respuestos La Tiendita**

*Última actualización: Julio 2026*
