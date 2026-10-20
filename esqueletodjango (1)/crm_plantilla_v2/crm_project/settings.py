"""
CONFIGURACIÓN DEL CRM (archivo ya completo; solo tocarás las marcadas con  >>> ALUMNO).
"""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent   # Carpeta raíz del proyecto

SECRET_KEY = 'clave-solo-para-desarrollo-cambiar-en-produccion'  # Nunca subir una real a GitHub
DEBUG = True                 # True = muestra errores detallados (solo desarrollo). False en producción
ALLOWED_HOSTS = []           # Con DEBUG=False hay que listar dominios, ej: ['midominio.com']

# >>> ALUMNO: nombre de tu CRM (aparece en la barra superior)
NOMBRE_CRM = 'Mi CRM'
# >>> ALUMNO: color principal en formato CSS. Valores válidos: '#0b6623', 'crimson', 'rgb(10,20,30)'...
COLOR_PRINCIPAL = '#2c3e50'

# >>> ALUMNO: MÓDULOS ACTIVOS. Cada nombre es una carpeta (app) del proyecto.
#   - Para DESACTIVAR un módulo: bórralo o coméntalo de la lista (y borra su bloque en contactos/detalle.html).
#   - Para CREAR uno nuevo:  python manage.py startapp nombre
#     y añade 'nombre' aquí + crea nombre/urls.py con app_name y una vista 'index'.
#   - El orden de la lista = el orden del menú.
MODULOS_CRM = [
    'contactos',
    'oportunidades',
    'interacciones',
    'tareas',
]

INSTALLED_APPS = [
    'django.contrib.admin',          # Panel /admin/
    'django.contrib.auth',           # Usuarios, login, permisos
    'django.contrib.contenttypes',   # Necesario para permisos/relaciones genéricas
    'django.contrib.sessions',       # Sesiones (mantener el login)
    'django.contrib.messages',       # Mensajes flash (messages.success(...))
    'django.contrib.staticfiles',    # CSS/JS/imágenes
    'core',                          # Inicio, login y plantilla base (NO tocar)
] + MODULOS_CRM

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',     # Protege formularios POST (usa {% csrf_token %})
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

ROOT_URLCONF = 'crm_project.urls'

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [],            # Carpetas extra de plantillas (opcional)
    'APP_DIRS': True,      # Busca en <app>/templates/ automáticamente
    'OPTIONS': {'context_processors': [
        'django.template.context_processors.request',
        'django.contrib.auth.context_processors.auth',
        'django.contrib.messages.context_processors.messages',
        'core.context_processors.crm',   # Pasa NOMBRE_CRM, COLOR y menú a todas las plantillas
    ]},
}]

WSGI_APPLICATION = 'crm_project.wsgi.application'

# Base de datos. Valores posibles de ENGINE:
#   'django.db.backends.sqlite3' (archivo, ideal para clase) | '...postgresql' | '...mysql'
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': BASE_DIR / 'db.sqlite3'}}

# >>> ALUMNO (opcional): idioma. Ej: 'es' (español), 'en-us', 'ca', 'fr'
LANGUAGE_CODE = 'es'
# Zona horaria. Ej: 'Europe/Madrid', 'UTC', 'America/Mexico_City'
TIME_ZONE = 'Europe/Madrid'
USE_I18N = True
USE_TZ = True          # True = guarda fechas en UTC (recomendado)

STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'   # Tipo de la clave primaria 'id'

# Login: a dónde ir si hace falta autenticarse / tras entrar / tras salir
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'inicio'
LOGOUT_REDIRECT_URL = 'login'
