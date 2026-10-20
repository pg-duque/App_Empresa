"""Define las direcciones web de la sección de oportunidades.
Se montan bajo /oportunidades/ desde crm_project/urls.py.
Por eso, la ruta '' de abajo corresponde a /oportunidades/.
"""

# Importa la función path, que sirve para asociar direcciones web con funciones.
from django.urls import path

# Importa las vistas de esta misma aplicación.
# Las vistas son funciones que reciben una petición y preparan una respuesta.
from . import views


# Nombre de la aplicación. Permite referirse a sus direcciones con un prefijo,
# por ejemplo: {% url 'oportunidades:index' %}.
app_name = 'oportunidades'


# Lista de rutas de esta aplicación.
urlpatterns = [
    # La ruta vacía representa /oportunidades/ y llama a views.index.
    # name='index' permite encontrar esta ruta por su nombre en plantillas y código.
    path('', views.index, name='index'),

    # /oportunidades/nuevo/ llama a la vista que crea una oportunidad.
    path('nuevo/', views.crear, name='crear'),

    # <int:pk> captura un número entero de la dirección y lo guarda en la variable pk.
    # Por ejemplo, /oportunidades/3/ llama a views.detalle(pk=3).
    path('<int:pk>/', views.detalle, name='detalle'),

    # /oportunidades/3/editar/ llama a views.editar con pk=3.
    path('<int:pk>/editar/', views.editar, name='editar'),

    # /oportunidades/3/borrar/ llama a views.borrar con pk=3.
    path('<int:pk>/borrar/', views.borrar, name='borrar'),

    # Otros convertidores disponibles:
    # <str:x> acepta texto; <slug:x>, texto con letras, números y guiones;
    # <uuid:x>, un identificador UUID.
]
