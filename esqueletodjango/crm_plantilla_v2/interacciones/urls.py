"""Define las direcciones web de la sección de interacciones.
Se montan bajo /interacciones/ desde crm_project/urls.py.
"""

# Importa la función path para conectar direcciones web con vistas.
from django.urls import path

# Importa las vistas de esta aplicación.
from . import views


# Nombre de la aplicación. Permite referirse a sus rutas por nombre,
# por ejemplo: {% url 'interacciones:index' %}.
app_name = 'interacciones'


# Lista de rutas de esta aplicación.
urlpatterns = [
    # La ruta vacía corresponde a /interacciones/ y muestra el listado.
    path('', views.index, name='index'),

    # /interacciones/nuevo/ muestra el formulario para crear una interacción.
    path('nuevo/', views.crear, name='crear'),

    # <int:pk> captura un número entero de la dirección y lo pasa a la vista
    # como pk. Por ejemplo, /interacciones/3/ llama a detalle con pk=3.
    path('<int:pk>/', views.detalle, name='detalle'),

    # /interacciones/3/editar/ abre el formulario para editar esa interacción.
    path('<int:pk>/editar/', views.editar, name='editar'),

    # /interacciones/3/borrar/ abre la página para borrar esa interacción.
    path('<int:pk>/borrar/', views.borrar, name='borrar'),

    # Otros convertidores:
    # <str:x> acepta texto.
    # <slug:x> acepta texto apto para direcciones web, normalmente con guiones.
    # <uuid:x> acepta un identificador UUID.
]
