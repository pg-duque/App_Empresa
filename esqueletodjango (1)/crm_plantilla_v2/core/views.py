from django.apps import apps
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render

def _modelo(app, nombre):
    """Devuelve el modelo o None si el módulo está desactivado en MODULOS_CRM (así el panel no se rompe)."""
    try:
        return apps.get_model(app, nombre)
    except LookupError:
        return None

@login_required   # Sin sesión iniciada -> redirige al login
def inicio(request):
    # Tarjetas con el número de objetos de cada módulo activo
    resumen = []
    for app, modelo, etiqueta in [('contactos', 'Contacto', 'Contactos'),
                                  ('oportunidades', 'Oportunidad', 'Oportunidades'),
                                  ('interacciones', 'Interaccion', 'Interacciones'),
                                  ('tareas', 'Tarea', 'Tareas')]:
        M = _modelo(app, modelo)
        if M:
            resumen.append({'etiqueta': etiqueta, 'n': M.objects.count(), 'url': f'{app}:index'})

    ultimas, pendientes, ganado = [], None, None
    Inter = _modelo('interacciones', 'Interaccion')
    if Inter:
        ultimas = Inter.objects.select_related('contacto')[:5]      # Últimas 5 (el modelo ya ordena por -fecha)
    Tarea = _modelo('tareas', 'Tarea')
    if Tarea:
        pendientes = Tarea.objects.filter(hecha=False).count()      # filter(campo=valor) = WHERE
    Op = _modelo('oportunidades', 'Oportunidad')
    if Op:
        ganado = Op.objects.filter(etapa='ganado').aggregate(t=Sum('importe'))['t'] or 0   # Sum = suma de la columna

    # TODO-ALUMNO 9: añade aquí tu propia métrica (ej: tareas vencidas, oportunidades por etapa...)
    return render(request, 'core/inicio.html', {
        'resumen': resumen, 'ultimas': ultimas, 'pendientes': pendientes, 'ganado': ganado})
