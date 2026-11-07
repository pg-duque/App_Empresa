"""
ADMIN: gestión rápida de datos en /admin/ sin escribir vistas.
"""
from django.contrib import admin
from .models import Contacto


@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    # TODO-ALUMNO 2: muestra cuota, sistema preferido y notas junto a los datos básicos.
    list_display = ('nombre', 'tipo', 'email', 'telefono', 'cuota_mensual', 'sistema_preferido', 'notas')        # Columnas del listado
    # Permite limitar los contactos por tipo, estado de pago o juego preferido en /admin/.
    list_filter = ('tipo', 'cuota_mensual', 'sistema_preferido')        # Filtros laterales
    # La búsqueda del administrador admite también el sistema de juego del contacto.
    search_fields = ('nombre', 'email', 'sistema_preferido')       # Caja de búsqueda ('^campo' empieza por · '=campo' exacto · 'relacion__campo')
    # Más opciones: ordering = (...) · list_editable = ('campo',) · date_hierarchy = 'fecha' · readonly_fields = (...)
