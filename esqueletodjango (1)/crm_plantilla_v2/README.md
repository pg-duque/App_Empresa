# CRM Django – Plantilla v2 (con ejemplo funcionando)

## Arrancar (1 comando)
- Linux/Mac: `bash iniciar.sh`
- Windows: `iniciar.bat`

Abre http://127.0.0.1:8000/ · usuario **admin** · clave **admin1234**

Manual: `pip install -r requirements.txt` → `python manage.py makemigrations` → `migrate` → `cargar_ejemplo` → `runserver`.

## Qué ya funciona
Login, panel con métricas y, en los 4 módulos (contactos, oportunidades, interacciones, tareas): listado con búsqueda, ficha, crear, editar y borrar. La ficha del contacto muestra su historial. Datos de ejemplo cargados.

## Qué haces tú
Lee **ENUNCIADO.md** y busca `TODO-ALUMNO` en el código (en VS Code: Ctrl+Shift+F).

## Mapa de archivos (por módulo)
models.py (tablas) · forms.py (formularios) · admin.py (panel /admin) · views.py (lógica) · urls.py (rutas) · templates/ (HTML)
