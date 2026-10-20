"""
ADMIN: gestión rápida de datos en /admin/ sin escribir vistas.
"""
from django.contrib import admin
from .models import Contacto


@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'email', 'telefono',)        # Columnas del listado
    list_filter = ('tipo',)        # Filtros laterales
    search_fields = ('nombre', 'email',)       # Caja de búsqueda ('^campo' empieza por · '=campo' exacto · 'relacion__campo')
    # Más opciones: ordering = (...) · list_editable = ('campo',) · date_hierarchy = 'fecha' · readonly_fields = (...)
