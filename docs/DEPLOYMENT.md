# 🚀 Guía de Deployment - Respuestos La Tiendita

## Deployment en Producción

### Opción 1: Render.com (Recomendado para principiantes)

#### Paso 1: Preparar código

1. Crear cuenta en [render.com](https://render.com)
2. Conectar tu repositorio GitHub

#### Paso 2: Crear Web Service para Backend

1. Click en "New +" → "Web Service"
2. Seleccionar tu repositorio
3. Configurar:
   - **Name**: respuestos-backend
   - **Root Directory**: backend
   - **Build Command**: `pip install -r requirements.txt && alembic upgrade head`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
   - **Environment**: Python 3.11

4. Agregar variables de entorno:
   ```
   DATABASE_URL: postgresql://...
   SECRET_KEY: tu-secret-key-cambiado
   DEBUG: False
   ```

#### Paso 3: Crear Base de Datos PostgreSQL

1. Click en "New +" → "PostgreSQL"
2. Configurar:
   - **Name**: respuestos-db
   - **Region**: Elige la más cercana

3. Copiar `DATABASE_URL` y agregar al Web Service

#### Paso 4: Crear Web Service para Frontend

1. Click en "New +" → "Web Service"
2. Configurar:
   - **Name**: respuestos-frontend
   - **Root Directory**: frontend
   - **Build Command**: `npm install && npm run build`
   - **Start Command**: `npm install -g serve && serve -s dist -l 3000`

3. Agregar variable:
   ```
   VITE_API_URL: https://respuestos-backend.onrender.com
   ```

---

### Opción 2: Railway.app

#### Paso 1: Setup inicial

1. Crear cuenta en [railway.app](https://railway.app)
2. Conectar GitHub

#### Paso 2: Crear servicios

```bash
# Desde la CLI de Railway
railway init
```

#### Paso 3: Configurar railway.toml

```toml
[build]
builder = "dockerfile"
dockerfilePath = "backend/Dockerfile"

[deploy]
startCommand = "uvicorn app.main:app --host 0.0.0.0 --port 8000"
```

---

### Opción 3: DigitalOcean App Platform

#### Paso 1: Crear aplicación

1. Ir a DigitalOcean App Platform
2. Click en "Create App"
3. Conectar repositorio GitHub

#### Paso 2: Configurar servicios

Agregar dos componentes:
- Backend (Docker)
- Frontend (Node.js)

---

### Opción 4: AWS (Para producción escalable)

#### Servicios necesarios:
- **ECS Fargate** - Para contenedores
- **RDS** - PostgreSQL gestionado
- **CloudFront** - CDN para frontend
- **Route53** - DNS
- **ACM** - Certificados SSL

[Ver documentación completa de AWS...]

---

## Checklist Pre-Deployment

### Backend

- [ ] Cambiar `DEBUG = False`
- [ ] Cambiar `SECRET_KEY` a uno seguro
- [ ] Configurar `CORS_ORIGINS` correctamente
- [ ] Usar PostgreSQL (no SQLite)
- [ ] Configurar variables de entorno
- [ ] Ejecutar pruebas: `pytest`
- [ ] Linter: `flake8 app/`
- [ ] Configurar backups de BD
- [ ] Configurar logs centralizados
- [ ] SSL/HTTPS habilitado

### Frontend

- [ ] Configurar `VITE_API_URL` correcto
- [ ] Build optimizado: `npm run build`
- [ ] Verificar tamaño del bundle
- [ ] Minificación habilitada
- [ ] Service workers configurados (PWA)
- [ ] Pruebas pasando
- [ ] Cache headers configurados
- [ ] HTTPS habilitado

---

## Monitoreo en Producción

### Backend

```python
# Agregar a app/main.py
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

sentry_sdk.init(
    dsn="https://your-sentry-dsn@sentry.io/...",
    integrations=[FastApiIntegration()],
)
```

### Frontend

```javascript
// Agregar a src/main.tsx
import * as Sentry from "@sentry/react";

Sentry.init({
  dsn: "https://your-sentry-dsn@sentry.io/...",
  integrations: [new Sentry.Replay()],
});
```

---

## SSL/HTTPS

### Let's Encrypt (Gratuito)

```bash
# Con Certbot
certbot certonly --standalone -d tu-dominio.com
```

### Nginx como Reverse Proxy

```nginx
server {
    listen 443 ssl;
    server_name tu-dominio.com;

    ssl_certificate /etc/letsencrypt/live/tu-dominio.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/tu-dominio.com/privkey.pem;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
    }
}
```

---

## Backups

### PostgreSQL

```bash
# Backup diario
0 2 * * * pg_dump -U respuestos respuestos_db > /backups/db-$(date +\%Y\%m\%d).sql

# Restaurar
psql -U respuestos respuestos_db < /backups/db-20240101.sql
```

---

## Escalabilidad

### Horizontal Scaling

1. **Load Balancer** (nginx, HAProxy)
2. **Múltiples instancias backend**
3. **Redis** para sesiones compartidas
4. **Base de datos replicada**

### Caché

```python
# Agregar Redis al backend
from redis import Redis

redis_client = Redis.from_url("redis://...")
```

---

## Troubleshooting

### Error 502 Bad Gateway

- Verificar que el backend está corriendo
- Revisar logs del reverse proxy

### Lentitud

- Verificar índices de BD
- Agregar caché (Redis)
- Optimizar queries

### Base de datos llena

- Implementar rotación de logs
- Comprimir datos antiguos
- Aumentar espacio en disco

---

## Costos Estimados (Mensual)

| Servicio | Estimado |
|----------|----------|
| Backend (Render) | $7-12 |
| Frontend (Render) | $7-12 |
| Base de datos (Render) | $7-15 |
| Total | $21-39 USD |

---

## Soporte

Para soporte en deployment, contactar al equipo de DevOps.
