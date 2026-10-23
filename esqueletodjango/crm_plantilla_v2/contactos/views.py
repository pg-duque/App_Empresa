"""
VISTAS de Contactos: reciben la petición (request) y devuelven una respuesta (HTML o redirección).
CRUD completo ya funcionando: listar (index), ver (detalle), crear, editar y borrar.
"""
from django.contrib import messages                       # Avisos tipo "Guardado correctamente"
from django.contrib.auth.decorators import login_required  # Exige haber iniciado sesión
from django.shortcuts import render, get_object_or_404, redirect
from core.utils import campos_de
from .models import Contacto
from .forms import ContactoForm


@login_required
def index(request):
    """LISTADO con búsqueda: /contactos/?q=texto"""
    q = request.GET.get('q', '').strip()             # request.GET = parámetros de la URL (?q=...)
    objetos = Contacto.objects.all()                # .all() = todos. Otros: .filter() .exclude() .get() .order_by('-campo') .count()
    if q:
        # __icontains = "contiene, sin distinguir mayúsculas". Otros: __exact __startswith __gt __lt __gte __lte __in=[..] __isnull=True
        objetos = objetos.filter(nombre__icontains=q)
    # TODO-ALUMNO 7: añade un filtro por un campo con choices, ej: tipo = request.GET.get('tipo')
    return render(request, 'contactos/lista.html', {'objetos': objetos, 'q': q})


@login_required
def detalle(request, pk):
    """FICHA de un objeto. <int:pk> en la URL llega aquí como pk."""
    objeto = get_object_or_404(Contacto, pk=pk)     # Si no existe -> error 404 (en vez de romperse)
    return render(request, 'contactos/detalle.html', {'objeto': objeto, 'campos': campos_de(objeto), 'ns': 'contactos'})


@login_required
def crear(request):
    """CREAR. GET = muestra el formulario vacío. POST = el usuario lo envió."""
    form = ContactoForm(request.POST or None, initial={})   # initial = valores precargados
    if request.method == 'POST' and form.is_valid():          # is_valid() ejecuta las validaciones del modelo
        obj = form.save()
        messages.success(request, 'Creado correctamente')
        return redirect('contactos:detalle', pk=obj.pk)           # Redirigir tras POST evita reenvíos al recargar
    return render(request, 'core/form.html', {'form': form, 'titulo': 'Nuevo: contacto', 'volver': 'contactos:index'})


@login_required
def editar(request, pk):
    """EDITAR: igual que crear pero con instance=objeto existente."""
    objeto = get_object_or_404(Contacto, pk=pk)
    form = ContactoForm(request.POST or None, instance=objeto)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Cambios guardados')
        return redirect('contactos:detalle', pk=objeto.pk)
    return render(request, 'core/form.html', {'form': form, 'titulo': f'Editar: {objeto}', 'volver': 'contactos:index'})


@login_required
def borrar(request, pk):
    """BORRAR: GET pide confirmación; solo el POST borra de verdad."""
    objeto = get_object_or_404(Contacto, pk=pk)
    if request.method == 'POST':
        objeto.delete()
        messages.success(request, 'Eliminado')
        return redirect('contactos:index')
    return render(request, 'core/confirmar_borrado.html', {'objeto': objeto, 'volver': 'contactos:index'})
