# Respuestos La Tiendita - Sistema ERP Profesional

## Stack Tecnológico Completo

✅ **Backend**: FastAPI + PostgreSQL + SQLAlchemy
✅ **Frontend**: React 18 + TypeScript + Tailwind CSS  
✅ **Autenticación**: JWT + Bcrypt
✅ **DevOps**: Docker + Docker Compose
✅ **Testing**: Pytest + Jest
✅ **Documentación**: OpenAPI/Swagger + Markdown

## 🚀 Inicio Rápido

### Con Docker (Recomendado)

```bash
# 1. Clonar y navegar
git clone https://github.com/kiki19R/Respuestos-la-tiendita-.git
cd Respuestos-la-tiendita-

# 2. Ejecutar setup
bash setup.sh

# 3. Acceder a la aplicación
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# API Docs: http://localhost:8000/api/docs
```

### Sin Docker

Ver [SETUP.md](./SETUP.md) para instrucciones detalladas.

## 📚 Documentación

- [Guía de Instalación](./SETUP.md)
- [Documentación API](./docs/API.md)
- [Arquitectura del Sistema](./docs/ARCHITECTURE.md)
- [Guía de Deployment](./docs/DEPLOYMENT.md)
- [README Principal](./README.md)

## 🔑 Credenciales de Prueba

**Email**: admin@example.com  
**Contraseña**: admin123456

## 📦 Estructura del Proyecto

```
.
├── backend/              # FastAPI + PostgreSQL
├── frontend/             # React + TypeScript
├── docker-compose.yml    # Orquestación de servicios
├── setup.sh              # Script de instalación
├── cleanup.sh            # Script de limpieza
├── SETUP.md              # Guía de setup
├── README.md             # README principal
└── docs/                 # Documentación adicional
    ├── API.md
    ├── ARCHITECTURE.md
    └── DEPLOYMENT.md
```

## ⚙️ Servicios Disponibles

| Servicio | URL | Puerto |
|----------|-----|--------|
| Frontend | http://localhost:3000 | 3000 |
| Backend | http://localhost:8000 | 8000 |
| API Docs | http://localhost:8000/api/docs | 8000 |
| pgAdmin | http://localhost:5050 | 5050 |
| PostgreSQL | localhost | 5432 |
| Redis | localhost | 6379 |

## 🛑 Detener Servicios

```bash
bash cleanup.sh
```

## 🤝 Contribuir

Los pull requests son bienvenidos. Abre un issue para discutir cambios importantes.

## 📄 Licencia

MIT License - Ver LICENSE para detalles

---

**Hecho con ❤️ para Respuestos La Tiendita**
