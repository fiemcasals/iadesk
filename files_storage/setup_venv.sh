#!/bin/bash

# Script para crear y activar venv con dependencias instaladas

echo "🔨 Creando virtual environment..."
python3 -m venv venv

echo "✅ Activando venv..."
source venv/bin/activate

echo "📦 Instalando dependencias..."
pip install --upgrade pip
pip install reportlab

echo "✨ Setup completado. Virtual environment activo."
echo "💡 Para desactivar en el futuro, ejecuta: deactivate"
