@echo off
REM Script para crear y activar venv con dependencias instaladas (Windows)

echo 🔨 Creando virtual environment...
python -m venv venv

echo ✅ Activando venv...
call venv\Scripts\activate.bat

echo 📦 Instalando dependencias...
pip install --upgrade pip
pip install reportlab

echo ✨ Setup completado. Virtual environment activo.
echo 💡 Para desactivar en el futuro, ejecuta: deactivate
pause
