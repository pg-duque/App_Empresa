# Importa la clase base para configurar una aplicación de Django.
from django.apps import AppConfig


# Define la configuración de la aplicación llamada "tareas".
class TareasConfig(AppConfig):

    # Tipo de campo que Django usará por defecto para los identificadores
    # automáticos (por ejemplo, el campo id de los modelos).
    default_auto_field = 'django.db.models.BigAutoField'

    # Nombre de la aplicación. Debe coincidir con el nombre de su carpeta.
    name = 'tareas'
