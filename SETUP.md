# 🚀 Guía de Instalación - Respuestos La Tiendita

## Requisitos Previos

- Docker y Docker Compose instalados
- Git
- Node.js 18+ (solo si ejecutas localmente sin Docker)
- Python 3.11+ (solo si ejecutas localmente sin Docker)

## Instalación Rápida con Docker (Recomendado)

### 1. Clonar el repositorio

```bash
git clone https://github.com/kiki19R/Respuestos-la-tiendita-.git
cd Respuestos-la-tiendita-
```

### 2. Configurar variables de entorno

```bash
# Copiar archivos de ejemplo
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

### 3. Ejecutar con Docker Compose

```bash
docker-compose up -d
```

### 4. Crear primer usuario (administrador)

```bash
# Acceder al contenedor del backend
docker-compose exec backend bash

# Dentro del contenedor
python -c "
from app.database import SessionLocal
from app.core.security import hash_password
from app.models.usuario import Usuario

db = SessionLocal()
usuario = Usuario(
    email='admin@example.com',
    nombre_completo='Administrador',
    contrasena_hash=hash_password('admin123456'),
    rol='admin',
    activo=True
)
db.add(usuario)
db.commit()
print('✅ Usuario administrador creado exitosamente')
"
```

### 5. Acceder a la aplicación

**Frontend:** http://localhost:3000
**Backend API:** http://localhost:8000
**Documentación API:** http://localhost:8000/api/docs
**pgAdmin:** http://localhost:5050

---

## Instalación Local (Sin Docker)

### Backend FastAPI

```bash
cd backend

# Crear ambiente virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar base de datos
# Asegúrate de tener PostgreSQL corriendo localmente
# y crear una BD: respuestos_db

# Ejecutar migraciones
alembic upgrade head

# Iniciar servidor
uvicorn app.main:app --reload
```

### Frontend React

```bash
cd frontend

# Instalar dependencias
npm install

# Iniciar servidor de desarrollo
npm run dev
```

---

## Credenciales de Ejemplo

| Campo | Valor |
|-------|-------|
| Email | admin@example.com |
| Contraseña | admin123456 |
| Rol | admin |

---

## Variables de Entorno

### Backend (.env)

```ini
APP_NAME=Respuestos La Tiendita
DATABASE_URL=postgresql://respuestos:respuestos_pass_123@localhost:5432/respuestos_db
SECRET_KEY=tu-secret-key-super-seguro-cambiar-en-produccion
DEBUG=False
CORS_ORIGINS=["http://localhost:3000", "http://localhost:5173"]
```

### Frontend (.env)

```ini
VITE_API_URL=http://localhost:8000
```

---

## Comandos Útiles

### Ver logs

```bash
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Detener servicios

```bash
docker-compose down
```

### Eliminar volúmenes (cuidado - elimina datos)

```bash
docker-compose down -v
```

### Reconstruir contenedores

```bash
docker-compose up -d --build
```

---

## Solución de Problemas

### Error: "Connection refused" en PostgreSQL

```bash
# Asegúrate de que postgres está corriendo
docker-compose ps

# Si no, reinicia los servicios
docker-compose restart postgres
```

### Error: Puerto 8000 ya en uso

```bash
# Cambiar puerto en docker-compose.yml
# Cambiar "8000:8000" a "8001:8000"
```

### Frontend no puede conectarse con backend

```bash
# Verificar que VITE_API_URL está correcto en frontend/.env
VITE_API_URL=http://localhost:8000
```

---

## Próximos Pasos

1. Crear usuarios adicionales (gerentes, vendedores)
2. Registrar proveedores y clientes
3. Agregar productos al catálogo
4. Comenzar con ventas y control de inventario

---

## Documentación Adicional

- [API Documentation](./docs/API.md)
- [Architecture](./docs/ARCHITECTURE.md)
- [Deployment Guide](./docs/DEPLOYMENT.md)
