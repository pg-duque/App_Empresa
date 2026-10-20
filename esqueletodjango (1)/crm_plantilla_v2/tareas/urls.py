"""Define las direcciones web de la sección de tareas.
Se montan bajo /tareas/ desde crm_project/urls.py.
"""

# Importa la función path para conectar direcciones web con vistas.
from django.urls import path

# Importa las vistas de esta aplicación.
from . import views


# Nombre de esta aplicación. Sirve para referirse a sus rutas
# por nombre, por ejemplo: {% url 'tareas:index' %}.
app_name = 'tareas'


# Lista de rutas de la aplicación.
urlpatterns = [
    # La ruta vacía corresponde a /tareas/ y muestra el listado.
    path('', views.index, name='index'),

    # /tareas/nuevo/ muestra el formulario para crear una tarea.
    path('nuevo/', views.crear, name='crear'),

    # <int:pk> captura un número entero de la dirección y lo pasa a la vista
    # como el argumento pk. Por ejemplo, /tareas/3/ llama a detalle con pk=3.
    path('<int:pk>/', views.detalle, name='detalle'),

    # /tareas/3/editar/ abre el formulario para editar la tarea con identificador 3.
    path('<int:pk>/editar/', views.editar, name='editar'),

    # /tareas/3/borrar/ abre la página para borrar la tarea con identificador 3.
    path('<int:pk>/borrar/', views.borrar, name='borrar'),

    # Otros convertidores:
    # <str:x> acepta texto.
    # <slug:x> acepta texto apto para direcciones web, normalmente con guiones.
    # <uuid:x> acepta un identificador UUID.
]
