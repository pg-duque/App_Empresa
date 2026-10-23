"""
URLs raíz. Registra automáticamente las URLs de cada módulo activo en settings.MODULOS_CRM.
Resultado: /contactos/, /oportunidades/, ... (no hace falta tocar este archivo)
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),   # Inicio + login/logout
]
for modulo in settings.MODULOS_CRM:
    # path('contactos/', include('contactos.urls')) generado en bucle
    urlpatterns.append(path(f'{modulo}/', include(f'{modulo}.urls')))
