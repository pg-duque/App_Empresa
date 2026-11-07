"""
VISTAS de Oportunidades: reciben una petición del navegador (request)
y devuelven una respuesta, como una página HTML o una redirección.
CRUD significa crear, leer, actualizar y borrar.
"""


# Permite mostrar avisos temporales, como «Guardado correctamente».
from django.contrib import messages
from django.views.decorators.http import require_POST  # Rechaza GET en acciones que guardan cambios.

# Hace que solo puedan entrar usuarios que hayan iniciado sesión.
from django.contrib.auth.decorators import login_required

# Herramientas para mostrar plantillas, buscar objetos o redirigir a otra página.
from django.shortcuts import render, get_object_or_404, redirect

# Función del proyecto que prepara los campos de un objeto para mostrarlos.
from core.utils import campos_de

# Importa el modelo y el formulario de esta aplicación.
from .models import Oportunidad
from .forms import OportunidadForm


# Protege esta vista: si el usuario no ha iniciado sesión, Django no la muestra.
@login_required
def index(request):
    """Muestra el listado. También permite buscar con /oportunidades/?q=texto."""

    # Lee el parámetro q de la URL. Si no existe, usa texto vacío.
    # strip() quita espacios sobrantes al principio y al final.
    q = request.GET.get('q', '').strip()

    # Obtiene todas las oportunidades de la base de datos.
    objetos = Oportunidad.objects.all()

    # Solo aplica la búsqueda si q contiene algún texto.
    if q:
        # Busca oportunidades cuyo título contenga q, ignorando mayúsculas y minúsculas.
        # __icontains es un filtro especial de Django para ese tipo de búsqueda.
        objetos = objetos.filter(titulo__icontains=q)

    # TODO-ALUMNO 7: lee y valida la etapa elegida en el desplegable.
    etapa = request.GET.get('etapa', '').strip()
    # dict convierte los pares de choices en un diccionario de valores permitidos.
    if etapa not in dict(Oportunidad.ETAPAS):
        etapa = ''  # Descarta valores de URL que no existen en el modelo.
    # Solo limita la consulta si se ha elegido una etapa válida.
    if etapa:
        objetos = objetos.filter(etapa=etapa)  # Se combina con la búsqueda por título.

    # Carga la plantilla lista.html y le entrega los datos que necesita:
    # objetos = oportunidades encontradas; q = texto buscado.
    # etapa conserva la selección; etapas proporciona las opciones del desplegable.
    return render(
        request,
        'oportunidades/lista.html',
        {'objetos': objetos, 'q': q, 'etapa': etapa, 'etapas': Oportunidad.ETAPAS}
    )


# Solo permite acceder a esta vista después de iniciar sesión.
@login_required
def detalle(request, pk):
    """Muestra la ficha de una oportunidad. pk es su identificador."""

    # Busca la oportunidad cuyo identificador coincide con pk.
    # Si no existe, muestra una página de error 404 («no encontrado»).
    objeto = get_object_or_404(Oportunidad, pk=pk)

    # Muestra la plantilla de detalle y le pasa:
    # objeto = oportunidad; campos = datos preparados para mostrar;
    # ns = nombre del espacio de nombres de sus direcciones web.
    return render(
        request,
        'oportunidades/detalle.html',
        {
            'objeto': objeto,
            'campos': campos_de(objeto),
            'ns': 'oportunidades'
        }
    )


# Solo permite acceder a esta vista después de iniciar sesión.
@login_required
def crear(request):
    """Muestra un formulario vacío y, cuando se envía, crea una oportunidad."""

    # request.POST contiene los datos si el formulario se envió.
    # Si no se envió, None hace que se muestre vacío.
    # initial precarga el contacto indicado en la URL, por ejemplo:
    # /oportunidades/nuevo/?contacto=3
    form = OportunidadForm(
        request.POST or None,
        initial={'contacto': request.GET.get('contacto')}
    )

    # Comprueba que el formulario se haya enviado con POST
    # y que todos sus datos pasen las validaciones.
    if request.method == 'POST' and form.is_valid():

        # Guarda la nueva oportunidad en la base de datos.
        obj = form.save()

        # Añade un mensaje de éxito para mostrarlo en la siguiente página.
        messages.success(request, 'Creado correctamente')

        # Redirige a la ficha recién creada.
        # obj.pk es su identificador. Redirigir después de guardar evita
        # que recargar la página vuelva a enviar el formulario.
        return redirect('oportunidades:detalle', pk=obj.pk)

    # Si el formulario no se ha enviado o tiene errores, muestra la página
    # del formulario con su título y la dirección para volver al listado.
    return render(
        request,
        'core/form.html',
        {
            'form': form,
            'titulo': 'Nuevo: oportunidad',
            'volver': 'oportunidades:index'
        }
    )


# Solo permite acceder a esta vista después de iniciar sesión.
@login_required
def editar(request, pk):
    """Muestra el formulario de una oportunidad existente y guarda los cambios."""

    # Busca la oportunidad que se quiere editar.
    # Si no existe, responde con un error 404.
    objeto = get_object_or_404(Oportunidad, pk=pk)

    # Crea el formulario usando los datos enviados, si los hay.
    # instance=objeto indica que se editará ese objeto existente,
    # en vez de crear uno nuevo.
    form = OportunidadForm(request.POST or None, instance=objeto)

    # Si el usuario envió el formulario y los datos son válidos:
    if request.method == 'POST' and form.is_valid():

        # Guarda los cambios en la oportunidad existente.
        form.save()

        # Añade un aviso de éxito.
        messages.success(request, 'Cambios guardados')

        # Vuelve a la ficha de la oportunidad editada.
        return redirect('oportunidades:detalle', pk=objeto.pk)

    # Muestra el formulario, tanto al abrirlo como si contiene errores.
    # f'Editar: {objeto}' construye un texto con el título de la oportunidad.
    return render(
        request,
        'core/form.html',
        {
            'form': form,
            'titulo': f'Editar: {objeto}',
            'volver': 'oportunidades:index'
        }
    )


# Solo permite acceder a esta vista después de iniciar sesión.
@login_required
def borrar(request, pk):
    """Pide confirmación al abrir la página y borra solo cuando se envía por POST."""

    # Busca la oportunidad que se quiere borrar.
    objeto = get_object_or_404(Oportunidad, pk=pk)

    # Solo borra si la petición es POST, normalmente al confirmar el formulario.
    # Así, visitar la dirección con GET no borra nada por accidente.
    if request.method == 'POST':

        # Elimina la oportunidad de la base de datos.
        objeto.delete()

        # Añade un aviso de que se eliminó.
        messages.success(request, 'Eliminado')

        # Vuelve al listado de oportunidades.
        return redirect('oportunidades:index')

    # Si la petición no es POST, muestra la página que pide confirmar el borrado.
    return render(
        request,
        'core/confirmar_borrado.html',
        {
            'objeto': objeto,
            'volver': 'oportunidades:index'
        }
    )


# TODO-ALUMNO 8: solo un usuario autenticado y una petición POST pueden ganar.
@login_required
# require_POST responde con 405 si se intenta guardar visitando una URL con GET.
@require_POST
def ganar(request, pk):
    """Marca como ganada usando la etapa de éxito de Modelmakers: fidelizado."""
    # Busca por identificador; devuelve 404 si la oportunidad ya no existe.
    objeto = get_object_or_404(Oportunidad, pk=pk)
    # Fidelizado es el valor guardado que representa una oportunidad ganada en este CRM.
    objeto.etapa = 'fidelizado'
    objeto.save(update_fields=['etapa'])  # Guarda únicamente la etapa.
    # El aviso se mostrará en la ficha después de la redirección.
    messages.success(request, 'Oportunidad ganada: contacto fidelizado.')
    # Vuelve a la ficha con GET para evitar reenviar el POST al recargar.
    return redirect('oportunidades:detalle', pk=objeto.pk)
