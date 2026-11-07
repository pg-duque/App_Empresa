"""
VISTAS de Eventos: reciben una petición del navegador (request)
y devuelven una respuesta, como una página HTML o una redirección.
CRUD significa crear, leer, actualizar y borrar.
"""

# Permite mostrar avisos temporales, por ejemplo «Guardado correctamente».
from django.contrib import messages

# Hace que solo puedan acceder usuarios que hayan iniciado sesión.
from django.contrib.auth.decorators import login_required

# Herramientas para mostrar páginas, buscar objetos y redirigir.
from django.shortcuts import render, get_object_or_404, redirect

# Función del proyecto que prepara los campos de un objeto para mostrarlos.
from core.utils import campos_de

# Importa el modelo y el formulario de eventos.
from .models import Evento
from .forms import EventoForm


# Protege esta vista: solo pueden verla usuarios con sesión iniciada.
@login_required
def index(request):
    """Muestra el listado de eventos y permite buscar: /eventos/?q=texto."""

    # Lee el parámetro q de la URL. Si no existe, usa texto vacío.
    # strip() quita espacios sobrantes al principio y al final.
    q = request.GET.get('q', '').strip()

    # Obtiene todos los eventos de la base de datos.
    objetos = Evento.objects.select_related('contacto').all()  # Carga el organizador sin consultas adicionales.

    # Si se escribió algo en la búsqueda, filtra los eventos.
    if q:
        # Busca títulos que contengan q, sin distinguir mayúsculas y minúsculas.
        objetos = objetos.filter(titulo__icontains=q)

    # Carga la plantilla del listado y le entrega los eventos y el texto buscado.
    return render(
        request,
        'eventos/lista.html',
        {'objetos': objetos, 'q': q}
    )


# Protege esta vista: solo pueden verla usuarios con sesión iniciada.
@login_required
def detalle(request, pk):
    """Muestra la ficha de un evento. pk es su identificador."""

    # Busca el evento con el identificador recibido en la URL.
    # Si no existe, muestra un error 404 («no encontrado»).
    objeto = get_object_or_404(Evento, pk=pk)

    # Muestra la plantilla de detalle y le pasa el evento,
    # sus campos preparados para mostrarse y el nombre de la aplicación.
    return render(
        request,
        'core/detalle.html',
        {
            'objeto': objeto,
            'campos': campos_de(objeto),
            'ns': 'eventos'
        }
    )


# Protege esta vista: solo pueden verla usuarios con sesión iniciada.
@login_required
def crear(request):
    """GET muestra el formulario; POST procesa los datos enviados."""

    # request.POST contiene los datos enviados por el formulario.
    # Si todavía no se ha enviado, None permite mostrar el formulario vacío.
    # initial precarga el contacto indicado en la URL, si lo hay.
    form = EventoForm(
        request.POST or None,
        initial={'contacto': request.GET.get('contacto')}
    )

    # Comprueba que el usuario haya enviado el formulario con POST
    # y que sus datos sean válidos.
    if request.method == 'POST' and form.is_valid():

        # Guarda el nuevo evento en la base de datos.
        obj = form.save()

        # Añade un aviso de que el evento se creó correctamente.
        messages.success(request, 'Creado correctamente')

        # Lleva al usuario a la ficha del evento recién creado.
        # Redirigir después de guardar evita repetir el envío al recargar.
        return redirect('eventos:detalle', pk=obj.pk)

    # Si aún no se envió el formulario o tiene errores, muestra la página
    # del formulario junto con su título y el enlace para volver al listado.
    return render(
        request,
        'core/form.html',
        {
            'form': form,
            'titulo': 'Nuevo: evento',
            'volver': 'eventos:index'
        }
    )


# Protege esta vista: solo pueden verla usuarios con sesión iniciada.
@login_required
def editar(request, pk):
    """Muestra y procesa el formulario para editar un evento existente."""

    # Busca el evento que se quiere editar; si no existe, devuelve un error 404.
    objeto = get_object_or_404(Evento, pk=pk)

    # Crea un formulario con los datos enviados, si los hay.
    # instance=objeto indica que se actualizará ese evento, no se creará otro.
    form = EventoForm(request.POST or None, instance=objeto)

    # Si se envió el formulario y todos los datos son válidos:
    if request.method == 'POST' and form.is_valid():

        # Guarda los cambios del evento existente.
        form.save()

        # Añade un aviso de que los cambios se guardaron.
        messages.success(request, 'Cambios guardados')

        # Redirige a la ficha del evento editado.
        return redirect('eventos:detalle', pk=objeto.pk)

    # Muestra el formulario de edición. Si hay errores, también aparecen aquí.
    # La f-string inserta el evento en el texto del título.
    return render(
        request,
        'core/form.html',
        {
            'form': form,
            'titulo': f'Editar: {objeto}',
            'volver': 'eventos:index'
        }
    )


# Protege esta vista: solo pueden verla usuarios con sesión iniciada.
@login_required
def borrar(request, pk):
    """GET muestra la confirmación; POST realiza el borrado."""

    # Busca el evento que se quiere borrar; si no existe, devuelve un error 404.
    objeto = get_object_or_404(Evento, pk=pk)

    # Solo borra cuando recibe una petición POST, normalmente al confirmar
    # el formulario. Abrir la página con GET no elimina nada.
    if request.method == 'POST':

        # Elimina el evento de la base de datos.
        objeto.delete()

        # Añade un aviso de que se eliminó correctamente.
        messages.success(request, 'Eliminado')

        # Redirige al listado de eventos.
        return redirect('eventos:index')

    # Si la petición no es POST, muestra la página que pide confirmar el borrado.
    return render(
        request,
        'core/confirmar_borrado.html',
        {
            'objeto': objeto,
            'volver': 'eventos:index'
        }
    )
