#!/bin/bash
# Instala Django en un entorno virtual SIN permisos de administrador.
# Uso (en Git Bash):   bash instalar_django.sh [carpeta] [nombre_proyecto]
# Ejemplo:             bash instalar_django.sh /c/Django miproyecto

CARPETA="${1:-$PWD/django-clase}"
PROYECTO="${2:-miproyecto}"

# 1. Buscar Python
if command -v python >/dev/null 2>&1 && python --version >/dev/null 2>&1; then
  PY=python
elif command -v py >/dev/null 2>&1; then
  PY=py
else
  echo "ERROR: no encuentro Python. Pregunta al profe o instala Python solo para tu usuario (sin admin)."
  exit 1
fi
echo ">> Usando: $($PY --version)"

# 2. Crear carpeta y entorno virtual
mkdir -p "$CARPETA" || { echo "ERROR: no puedo crear $CARPETA"; exit 1; }
cd "$CARPETA" || exit 1

if [ ! -d venv ]; then
  echo ">> Creando entorno virtual..."
  $PY -m venv venv || { echo "ERROR al crear el venv"; exit 1; }
fi

# 3. Localizar el python del venv (Windows: Scripts, Linux/Mac: bin)
if [ -f venv/Scripts/python.exe ]; then
  VPY="venv/Scripts/python.exe"
  ACTIVAR="source venv/Scripts/activate   (Git Bash)  |  .\\venv\\Scripts\\Activate.ps1  (PowerShell)"
else
  VPY="venv/bin/python"
  ACTIVAR="source venv/bin/activate"
fi

# 4. Instalar Django (version estable)
echo ">> Instalando Django..."
"$VPY" -m pip install --upgrade pip >/dev/null 2>&1
"$VPY" -m pip install django || { echo "ERROR instalando Django (¿hay proxy o no hay internet?)"; exit 1; }
echo ">> Version instalada: $("$VPY" -m django --version)"

# 5. Crear el proyecto si no existe
if [ ! -d "$PROYECTO" ]; then
  echo ">> Creando proyecto '$PROYECTO'..."
  "$VPY" -m django startproject "$PROYECTO"
fi

echo ""
echo "LISTO. Para trabajar:"
echo "  cd $CARPETA"
echo "  $ACTIVAR"
echo "  cd $PROYECTO"
echo "  python manage.py runserver"
echo "Y abre http://127.0.0.1:8000 en el navegador."
