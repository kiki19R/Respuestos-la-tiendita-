#!/bin/bash
# Script para iniciar el backend

echo "🚀 Iniciando backend FastAPI..."
echo "📍 Asegúrate de que PostgreSQL esté ejecutándose: docker-compose up -d"

# Crear tabla de base de datos
echo "🔧 Ejecutando migraciones de base de datos..."
alembic upgrade head

# Iniciar servidor
echo "✅ Iniciando servidor Uvicorn..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
