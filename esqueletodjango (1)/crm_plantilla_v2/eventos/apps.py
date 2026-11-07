"""Nivel 4: configuración del módulo independiente de actividades del club."""
# AppConfig permite que Django registre los modelos y plantillas de esta aplicación.
from django.apps import AppConfig


class EventosConfig(AppConfig):
    # Usa el mismo tipo de identificador automático que los demás módulos del CRM.
    default_auto_field = 'django.db.models.BigAutoField'
    # Coincide con el nombre de la carpeta y con su entrada en MODULOS_CRM.
    name = 'eventos'
    # Etiqueta legible en el administrador.
    verbose_name = 'Eventos del club'
