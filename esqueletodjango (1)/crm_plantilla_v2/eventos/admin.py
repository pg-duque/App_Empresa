"""Gestión de eventos desde /admin/, igual que los demás módulos."""
# Permite registrar el modelo en el administrador de Django.
from django.contrib import admin
# Modelo que se podrá gestionar desde el administrador.
from .models import Evento


# Vincula el modelo con sus columnas, filtros y búsqueda.
@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    # Datos principales de cada evento en la tabla del administrador.
    list_display = ('titulo', 'tipo', 'fecha', 'lugar', 'aforo', 'contacto')
    # Filtros por actividad y fecha para localizar los eventos del club.
    list_filter = ('tipo', 'fecha')
    # Busca también el lugar y el nombre del contacto organizador.
    search_fields = ('titulo', 'lugar', 'contacto__nombre')
