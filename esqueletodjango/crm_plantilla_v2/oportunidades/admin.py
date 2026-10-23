"""
ADMIN: gestión rápida de datos en /admin/ sin escribir vistas.
"""
from django.contrib import admin
from .models import Oportunidad


@admin.register(Oportunidad)
class OportunidadAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'contacto', 'etapa', 'importe',)        # Columnas del listado
    list_filter = ('etapa',)        # Filtros laterales
    search_fields = ('titulo', 'contacto__nombre',)       # Caja de búsqueda ('^campo' empieza por · '=campo' exacto · 'relacion__campo')
    # Más opciones: ordering = (...) · list_editable = ('campo',) · date_hierarchy = 'fecha' · readonly_fields = (...)
