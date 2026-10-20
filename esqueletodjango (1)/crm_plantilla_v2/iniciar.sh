#!/bin/bash
# Arranque en 1 comando (Linux/Mac):  bash iniciar.sh
python3 -m venv venv 2>/dev/null; source venv/bin/activate
pip install -q -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py cargar_ejemplo
echo "Abre http://127.0.0.1:8000/  usuario: admin  clave: admin1234"
python manage.py runserver
