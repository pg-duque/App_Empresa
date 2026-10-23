"""
VISTAS de Interacciones: reciben la petición (request) y devuelven una respuesta (HTML o redirección).
CRUD completo ya funcionando: listar (index), ver (detalle), crear, editar y borrar.
"""
# Importa el sistema de mensajes de Django para enseñar avisos al usuario
from django.contrib import messages

# Importa el decorador que obliga a estar logueado para entrar en estas vistas
from django.contrib.auth.decorators import login_required

# Importa herramientas útiles de Django:
# - render: pinta una plantilla HTML
# - get_object_or_404: busca un objeto o devuelve error 404 si no existe
# - redirect: manda al usuario a otra URL
from django.shortcuts import render, get_object_or_404, redirect

# Importa una función propia del proyecto para sacar los campos de un objeto
from core.utils import campos_de

# Importa el modelo Interaccion de esta app
from .models import Interaccion

# Importa el formulario de Interaccion
from .forms import InteraccionForm


# Esta vista solo la puede usar alguien logueado
@login_required
def index(request):
    """LISTADO con búsqueda: /interacciones/?q=texto"""
    # Lee el parámetro q de la URL. Si no existe, pone cadena vacía.
    # strip() quita espacios al principio y al final.
    q = request.GET.get('q', '').strip()

    # Trae todos los registros de Interaccion de la base de datos
    objetos = Interaccion.objects.all()

    # Si el usuario escribió algo en la búsqueda...
    if q:
        # Filtra los objetos cuyo campo "resumen" contenga el texto q
        # icontains = sin diferenciar mayúsculas/minúsculas
        objetos = objetos.filter(resumen__icontains=q)

    # TODO: aquí se podría añadir otro filtro, por ejemplo por "tipo"
    return render(request, 'interacciones/lista.html', {'objetos': objetos, 'q': q})


# Esta vista también exige login
@login_required
def detalle(request, pk):
    """FICHA de un objeto. <int:pk> en la URL llega aquí como pk."""
    # Busca la Interaccion con esa clave primaria.
    # Si no existe, Django devuelve una página 404.
    objeto = get_object_or_404(Interaccion, pk=pk)

    # Renderiza la plantilla de detalle enviándole:
    # - el objeto
    # - sus campos para mostrarlos
    # - ns = nombre de espacio o sección
    return render(
        request,
        'core/detalle.html',
        {'objeto': objeto, 'campos': campos_de(objeto), 'ns': 'interacciones'}
    )


# Esta vista crea una nueva Interaccion
@login_required
def crear(request):
    """CREAR. GET = muestra el formulario vacío. POST = el usuario lo envió."""
    # Si viene POST, usa los datos enviados.
    # Si no viene POST, el formulario sale vacío.
    # initial precarga el campo contacto con lo que venga en la URL.
    form = InteraccionForm(
        request.POST or None,
        initial={'contacto': request.GET.get('contacto')}
    )

    # Solo entra aquí si el formulario fue enviado por POST y es válido
    if request.method == 'POST' and form.is_valid():
        # commit=False significa: crea el objeto, pero todavía no lo guardes en la BD
        obj = form.save(commit=False)

        # Asigna como autor al usuario logueado
        obj.autor = request.user

        # Ahora sí, guarda el objeto en la base de datos
        obj.save()

        # Muestra un mensaje de éxito
        messages.success(request, 'Creado correctamente')

        # Redirige al detalle del objeto recién creado
        return redirect('interacciones:detalle', pk=obj.pk)

    # Si no es POST o el formulario es inválido, vuelve a mostrar el formulario
    return render(
        request,
        'core/form.html',
        {'form': form, 'titulo': 'Nuevo: interacción', 'volver': 'interacciones:index'}
    )


# Esta vista edita una Interaccion existente
@login_required
def editar(request, pk):
    """EDITAR: igual que crear pero con instance=objeto existente."""
    # Busca el objeto que se quiere editar
    objeto = get_object_or_404(Interaccion, pk=pk)

    # Crea el formulario con los datos del objeto existente
    # instance=objeto hace que el formulario venga rellenado
    form = InteraccionForm(request.POST or None, instance=objeto)

    # Si se envió el formulario y todo está bien...
    if request.method == 'POST' and form.is_valid():
        # Guarda los cambios en la BD
        form.save()

        # Mensaje de éxito
        messages.success(request, 'Cambios guardados')

        # Vuelve al detalle
        return redirect('interacciones:detalle', pk=objeto.pk)

    # Si no, enseña el formulario para editar
    return render(
        request,
        'core/form.html',
        {'form': form, 'titulo': f'Editar: {objeto}', 'volver': 'interacciones:index'}
    )


# Esta vista borra una Interaccion
@login_required
def borrar(request, pk):
    """BORRAR: GET pide confirmación; solo el POST borra de verdad."""
    # Busca el objeto a borrar
    objeto = get_object_or_404(Interaccion, pk=pk)

    # Si el usuario confirma enviando el formulario por POST...
    if request.method == 'POST':
        # Borra el objeto de la base de datos
        objeto.delete()

        # Mensaje de éxito
        messages.success(request, 'Eliminado')

        # Vuelve al listado
        return redirect('interacciones:index')

    # Si no han confirmado todavía, enseña una pantalla de confirmación
    return render(
        request,
        'core/confirmar_borrado.html',
        {'objeto': objeto, 'volver': 'interacciones:index'}
    )
