from django.conf import settings

def crm(request):
    """Datos disponibles en TODAS las plantillas: {{ NOMBRE_CRM }}, {{ COLOR }}, {{ modulos }}."""
    return {
        'NOMBRE_CRM': settings.NOMBRE_CRM,
        'COLOR': settings.COLOR_PRINCIPAL,
        'modulos': [{'nombre': m.capitalize(), 'url': f'{m}:index'} for m in settings.MODULOS_CRM],
    }
