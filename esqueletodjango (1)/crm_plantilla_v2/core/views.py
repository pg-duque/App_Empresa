from django.apps import apps
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils import timezone  # Usa la fecha de la zona horaria del CRM.
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

    # None permite ocultar métricas si su módulo está desactivado; ultimas empieza vacía.
    ultimas, pendientes, fidelizado, vencidas = [], None, None, None
    Inter = _modelo('interacciones', 'Interaccion')
    if Inter:
        ultimas = Inter.objects.select_related('contacto')[:5]      # Últimas 5 (el modelo ya ordena por -fecha)
    Tarea = _modelo('tareas', 'Tarea')
    if Tarea:
        # TODO-ALUMNO 9: hecha=False descarta las terminadas; __lt significa anterior a hoy.
        # localdate usa Europe/Madrid y count devuelve el número de tareas vencidas.
        vencidas = Tarea.objects.filter(hecha=False, vence__lt=timezone.localdate()).count()
        pendientes = Tarea.objects.filter(hecha=False).count()      # filter(campo=valor) = WHERE
    Op = _modelo('oportunidades', 'Oportunidad')
    if Op:
        # TODO-ALUMNO 3: suma solo la etapa de éxito personalizada; usa 0 si no hay importes.
        fidelizado = Op.objects.filter(etapa='fidelizado').aggregate(t=Sum('importe'))['t'] or 0   # Sum = suma de la columna

    # TODO-ALUMNO 9 completado: envía también el número de tareas vencidas.
    return render(request, 'core/inicio.html', {
        'resumen': resumen, 'ultimas': ultimas, 'pendientes': pendientes, 'fidelizado': fidelizado, 'vencidas': vencidas})
