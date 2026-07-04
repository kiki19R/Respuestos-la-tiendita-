#!/bin/bash
set -e

echo "🚀 Iniciando setup de Respuestos La Tiendita..."

# Verificar Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker no está instalado"
    exit 1
fi

echo "✅ Docker encontrado"

# Verificar Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose no está instalado"
    exit 1
fi

echo "✅ Docker Compose encontrado"

# Crear .env files si no existen
if [ ! -f "backend/.env" ]; then
    echo "📝 Creando backend/.env"
    cp backend/.env.example backend/.env
fi

if [ ! -f "frontend/.env" ]; then
    echo "📝 Creando frontend/.env"
    cp frontend/.env.example frontend/.env
fi

echo "🐳 Iniciando servicios con Docker Compose..."
docker-compose up -d

echo "⏳ Esperando que PostgreSQL esté listo..."
sleep 10

echo "✅ Servicios iniciados:"
echo "   - Frontend: http://localhost:3000"
echo "   - Backend: http://localhost:8000"
echo "   - API Docs: http://localhost:8000/api/docs"
echo "   - pgAdmin: http://localhost:5050"
echo ""
echo "🔑 Credenciales de prueba:"
echo "   Email: admin@example.com"
echo "   Password: admin123456"
echo ""
echo "📚 Para más información, ver SETUP.md"
