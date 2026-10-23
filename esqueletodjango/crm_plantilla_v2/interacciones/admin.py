"""
ADMIN: configuración para gestionar datos desde /admin/
sin tener que crear vistas propias.
"""

# Importa las herramientas del sitio de administración de Django.
from django.contrib import admin

# Importa el modelo Interaccion que se quiere administrar.
from .models import Interaccion


# Registra Interaccion en el administrador y le asigna esta configuración.
# Así aparecerá en /admin/ para poder consultarla y editarla.
@admin.register(Interaccion)
class InteraccionAdmin(admin.ModelAdmin):

    # Define las columnas que aparecerán en el listado de interacciones.
    list_display = ('fecha', 'contacto', 'canal', 'autor',)

    # Añade un filtro lateral para seleccionar interacciones por canal.
    list_filter = ('canal',)

    # Añade una caja de búsqueda.
    # Busca en el resumen y en el nombre del contacto relacionado.
    # contacto__nombre significa: entra en el campo contacto y busca por nombre.
    search_fields = ('resumen', 'contacto__nombre',)

    # Otras opciones que podrías añadir:
    # ordering = (...)                 ordena el listado.
    # list_editable = ('campo',)       permite editar ese campo desde el listado.
    # date_hierarchy = 'fecha'         añade navegación por fechas.
    # readonly_fields = (...)          muestra campos que no se pueden editar.
