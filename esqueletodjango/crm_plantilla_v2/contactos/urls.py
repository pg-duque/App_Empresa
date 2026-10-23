"""URLs de contactos (se montan bajo /contactos/ automáticamente desde crm_project/urls.py)."""
from django.urls import path
from . import views

app_name = 'contactos'   # Espacio de nombres: en plantillas {% url 'contactos:index' %}

urlpatterns = [
    path('', views.index, name='index'),                          # /contactos/
    path('nuevo/', views.crear, name='crear'),                    # /contactos/nuevo/
    path('<int:pk>/', views.detalle, name='detalle'),             # /contactos/3/   (<int:pk> = número entero)
    path('<int:pk>/editar/', views.editar, name='editar'),
    path('<int:pk>/borrar/', views.borrar, name='borrar'),
    # Otros convertidores: <str:x> texto · <slug:x> texto-con-guiones · <uuid:x>
]
