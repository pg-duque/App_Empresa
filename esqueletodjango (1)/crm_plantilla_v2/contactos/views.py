"""
VISTAS de Contactos: reciben la petición (request) y devuelven una respuesta (HTML o redirección).
CRUD completo ya funcionando: listar (index), ver (detalle), crear, editar y borrar.
"""
from django.contrib import messages                       # Avisos tipo "Guardado correctamente"
from django.contrib.auth.decorators import login_required  # Exige haber iniciado sesión
from django.shortcuts import render, get_object_or_404, redirect
import csv  # Escribe el archivo de contactos con separadores y comillas correctos.
from django.core.paginator import Paginator  # Divide el listado en páginas.
from django.http import HttpResponse  # Permite devolver un archivo descargable.
from core.utils import campos_de
from .models import Contacto
from .forms import ContactoForm


def contactos_filtrados(request):
    """Aplica la misma búsqueda y filtro al listado y a la exportación."""
    q = request.GET.get('q', '').strip()  # Conserva la búsqueda por nombre.
    tipo = request.GET.get('tipo', '').strip()  # Lee el desplegable de tipos.
    # Ignora valores ajenos a las opciones definidas en el modelo.
    if tipo not in dict(Contacto.TIPOS):
        tipo = ''  # Una opción desconocida equivale a mostrar todos los tipos.
    objetos = Contacto.objects.all()  # Consulta inicial, antes de aplicar condiciones.
    # Si hay texto, busca por nombre sin distinguir mayúsculas.
    if q:
        objetos = objetos.filter(nombre__icontains=q)
    # El tipo vacío deja todos los tipos; otro valor exige coincidencia exacta.
    if tipo:
        objetos = objetos.filter(tipo=tipo)  # Ambos filtros se combinan.
    return objetos, q, tipo  # Devuelve los resultados y las dos selecciones del usuario.


# Exige iniciar sesión antes de consultar el listado.
@login_required
def index(request):
    """TODO-ALUMNO 7 y nivel 3: filtra y muestra 10 contactos por página."""
    # Reutiliza los filtros para que el listado y el CSV muestren la misma selección.
    objetos, q, tipo = contactos_filtrados(request)
    # get_page acepta páginas vacías, incorrectas o fuera de rango sin fallar.
    pagina = Paginator(objetos, 10).get_page(request.GET.get('page'))
    # objetos contiene solo la página actual; pagina permite dibujar Anterior/Siguiente.
    # tipos rellena el desplegable y tipo/q mantienen los valores tras enviar el formulario.
    return render(request, 'contactos/lista.html', {
        'objetos': pagina, 'pagina': pagina, 'q': q,
        'tipo': tipo, 'tipos': Contacto.TIPOS,
    })


# La descarga de contactos también requiere una sesión iniciada.
@login_required
def exportar_csv(request):
    """Nivel 3: descarga todos los contactos que cumplen los filtros actuales."""
    # Exporta la consulta completa; los guiones bajos descartan valores que aquí no se usan.
    objetos, _, _ = contactos_filtrados(request)
    # Indica al navegador el formato del archivo y la codificación de las tildes.
    respuesta = HttpResponse(content_type='text/csv; charset=utf-8')
    # attachment solicita una descarga con el nombre contactos.csv.
    respuesta['Content-Disposition'] = 'attachment; filename="contactos.csv"'
    respuesta.write('\ufeff')  # Facilita que Excel reconozca las tildes.
    # El punto y coma separa columnas; csv.writer escapa comillas y saltos de línea.
    escritor = csv.writer(respuesta, delimiter=';')
    # Primera fila: títulos de las columnas en el mismo orden que los datos.
    escritor.writerow(['Nombre', 'Tipo', 'Email', 'Teléfono', 'Cuota mensual pagada',
                        'Sistema preferido', 'Notas'])
    # Recorre todos los contactos filtrados, aunque el listado tenga varias páginas.
    for contacto in objetos:
        # get_tipo_display muestra la etiqueta; la cuota se traduce a Sí/No.
        fila = [contacto.nombre, contacto.get_tipo_display(), contacto.email,
                contacto.telefono, 'Sí' if contacto.cuota_mensual else 'No',
                contacto.sistema_preferido, contacto.notas]
        # Evita que una hoja de cálculo interprete textos como fórmulas.
        fila = ["'" + valor if valor.lstrip().startswith(('=', '+', '-', '@'))
                else valor for valor in fila]
        escritor.writerow(fila)  # Añade el contacto como una fila del archivo.
    return respuesta  # Devuelve el archivo terminado al navegador.


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
