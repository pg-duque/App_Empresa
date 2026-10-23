"""
ADMIN: configuración para gestionar datos desde /admin/
sin tener que crear vistas propias.
"""

# Importa las herramientas del sitio de administración de Django.
from django.contrib import admin

# Importa el modelo Tarea que se quiere administrar.
from .models import Tarea


# Registra Tarea en el administrador y le asigna esta configuración.
# Así aparecerá en /admin/ y se podrá ver, crear y editar desde allí.
@admin.register(Tarea)
class TareaAdmin(admin.ModelAdmin):

    # Elige qué columnas aparecen en la lista de tareas.
    list_display = ('titulo', 'contacto', 'vence', 'hecha',)

    # Añade un filtro lateral para mostrar, por ejemplo,
    # solo las tareas hechas o solo las pendientes.
    list_filter = ('hecha',)

    # Añade una caja de búsqueda que busca en el campo titulo.
    # '^campo' busca valores que empiezan por el texto escrito.
    # '=campo' busca coincidencias exactas.
    # 'relacion__campo' busca en un campo del objeto relacionado.
    search_fields = ('titulo',)

    # Otras opciones que podrías añadir:
    # ordering = (...)              ordena el listado.
    # list_editable = ('campo',)    permite editar ese campo desde el listado.
    # date_hierarchy = 'fecha'      añade navegación por fechas.
    # readonly_fields = (...)       muestra campos que no se pueden editar.
