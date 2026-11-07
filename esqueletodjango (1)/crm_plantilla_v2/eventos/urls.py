"""Rutas del módulo; crm_project las monta automáticamente bajo /eventos/."""
# path relaciona una dirección con una función de vista.
from django.urls import path
# Importa las funciones que muestran y procesan las páginas de eventos.
from . import views

# Prefijo usado al generar enlaces, por ejemplo eventos:detalle.
app_name = 'eventos'
# Misma estructura de listado, ficha, alta, edición y borrado que tareas.
urlpatterns = [
    path('', views.index, name='index'),  # Listado y búsqueda.
    path('nuevo/', views.crear, name='crear'),  # Formulario de alta.
    path('<int:pk>/', views.detalle, name='detalle'),  # Ficha por identificador.
    path('<int:pk>/editar/', views.editar, name='editar'),  # Formulario de edición.
    path('<int:pk>/borrar/', views.borrar, name='borrar'),  # Confirmación y borrado por POST.
]
