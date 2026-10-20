# Importa la clase base que Django usa para configurar una aplicación.
from django.apps import AppConfig


# Define la configuración de la aplicación llamada "interacciones".
class InteraccionesConfig(AppConfig):

    # Tipo de campo que Django usará por defecto para los identificadores
    # automáticos de los modelos, como el campo id.
    default_auto_field = 'django.db.models.BigAutoField'

    # Nombre de la aplicación; debe coincidir con el nombre de su carpeta.
    name = 'interacciones'
