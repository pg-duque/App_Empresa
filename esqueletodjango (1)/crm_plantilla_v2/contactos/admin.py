"""
ADMIN: gestión rápida de datos en /admin/ sin escribir vistas.
"""
from django.contrib import admin
from .models import Contacto


@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'email', 'telefono', 'cuota_mesnual', 'sistema_preferido')        # Columnas del listado
    list_filter = ('tipo', 'cuota_mesnual', 'sistema_preferido')        # Filtros laterales
    search_fields = ('nombre', 'email', 'sistema_preferido')       # Caja de búsqueda ('^campo' empieza por · '=campo' exacto · 'relacion__campo')
    # Más opciones: ordering = (...) · list_editable = ('campo',) · date_hierarchy = 'fecha' · readonly_fields = (...)
