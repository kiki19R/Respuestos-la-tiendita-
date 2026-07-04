#!/bin/bash
set -e

echo "🧹 Limpiando recursos de Docker..."

echo "⏹️  Deteniendo contenedores..."
docker-compose down

echo "🗑️  ¿Deseas eliminar volúmenes (datos)? (s/n)"
read -r response

if [ "$response" = "s" ]; then
    echo "🗑️  Eliminando volúmenes..."
    docker-compose down -v
fi

echo "✅ Limpieza completada"
