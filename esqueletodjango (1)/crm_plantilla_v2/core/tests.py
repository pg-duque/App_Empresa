"""Pruebas de los requisitos de clase; usan una base temporal, sin tocar datos reales."""
# Lector CSV para verificar las columnas y los caracteres especiales exportados.
import csv
# Flujos de texto en memoria: no es necesario crear archivos para comprobar el CSV.
import io
# timedelta permite preparar vencimientos anteriores y posteriores a hoy.
from datetime import timedelta
# Decimal permite comparar importes exactos sin errores de coma flotante.
from decimal import Decimal
# Carga por nombre la migración cuyo archivo comienza por un número.
from importlib import import_module

# Registro de modelos que recibe la función de migración.
from django.apps import apps
# Usuario de pruebas para verificar las páginas que requieren sesión.
from django.contrib.auth.models import User
# Ejecuta cargar_ejemplo desde la prueba como si se llamara con manage.py.
from django.core.management import call_command
# Proporciona la conexión de la base temporal usada para probar la migración.
from django.db import connection
# TestCase aísla los datos; Client simula peticiones, incluida la comprobación CSRF.
from django.test import Client, TestCase
# reverse resuelve las rutas por nombre para no escribir direcciones a mano.
from django.urls import reverse
# Fecha actual según la zona horaria configurada para el CRM.
from django.utils import timezone

# Formulario de contacto: permite comprobar que incluye los campos personalizados.
from contactos.forms import ContactoForm
# Modelo con el que se crean contactos de prueba y se validan sus campos.
from contactos.models import Contacto
# Modelo usado para verificar el canal y la asignación del autor.
from interacciones.models import Interaccion
# Modelo usado para comprobar etapas, importes y cambios al ganar.
from oportunidades.models import Oportunidad
# Formulario de tarea: permite comprobar la presencia de prioridad.
from tareas.forms import TareaForm
# Modelo usado para preparar tareas y comprobar que el formulario las guarda.
from tareas.models import Tarea


# Agrupa pruebas de funciones del CRM.
class RequisitosCRMTests(TestCase):
    """Comprueba filtros combinados, exportación, paginación y acciones protegidas."""

    # Prepara un usuario autenticado, dos tipos de contacto y una oportunidad antes de cada prueba.
    def setUp(self):
        # Crea datos aislados con los campos necesarios para este caso de prueba.
        self.usuario = User.objects.create_user('alumno', password='prueba-clase')
        # Autentica al cliente de prueba para acceder a las vistas protegidas.
        self.client.force_login(self.usuario)
        # Crea datos aislados con los campos necesarios para este caso de prueba.
        self.socio = Contacto.objects.create(nombre='Ana club', tipo='socio',
                                             cuota_mensual=True, sistema_preferido='X-Wing')
        # Crea datos aislados con los campos necesarios para este caso de prueba.
        self.jugador = Contacto.objects.create(nombre='Ana jugadora', tipo='jugador')
        # Crea datos aislados con los campos necesarios para este caso de prueba.
        self.op = Oportunidad.objects.create(titulo='Pedido pinturas', contacto=self.socio,
                                             etapa='en_proceso', importe=Decimal('125.50'))

    # Comprueba la intersección de nombre/tipo y que la pantalla conserva la opción seleccionada.
    def test_filtros_contactos_combinados_y_seleccion(self):
        # Añade un registro de contraste para comprobar que los filtros incluyen y excluyen correctamente.
        Contacto.objects.create(nombre='Otro socio', tipo='socio')
        # Solicita la página y conserva la respuesta para comprobar su contenido y contexto.
        r = self.client.get(reverse('contactos:index'), {'q': '  ANA  ', 'tipo': 'socio'})
        # Compara el resultado con el valor esperado para detectar un error en este requisito.
        self.assertEqual([o.pk for o in r.context['objetos']], [self.socio.pk])
        # Verifica que el HTML contiene el dato esperado o que oculta una acción que ya no corresponde.
        self.assertContains(r, 'value="socio" selected')
        # Verifica que el HTML contiene el dato esperado o que oculta una acción que ya no corresponde.
        self.assertContains(r, 'X-Wing')
        # Verifica que el HTML contiene el dato esperado o que oculta una acción que ya no corresponde.
        self.assertContains(r, 'Cuota pagada')

    # Prueba el listado completo, la búsqueda vacía y el descarte de tipos desconocidos.
    def test_todos_sin_resultados_y_opciones_invalidas(self):
        # Compara el resultado con el valor esperado para detectar un error en este requisito.
        self.assertEqual(self.client.get(reverse('contactos:index')).context['pagina'].paginator.count, 2)
        # Solicita la página y conserva la respuesta para comprobar su contenido y contexto.
        r = self.client.get(reverse('contactos:index'), {'q': 'inexistente', 'tipo': 'socio'})
        # Verifica que el HTML contiene el dato esperado o que oculta una acción que ya no corresponde.
        self.assertContains(r, 'No hay contactos que coincidan')
        # Solicita la página y conserva la respuesta para comprobar su contenido y contexto.
        r = self.client.get(reverse('contactos:index'), {'tipo': 'inventado'})
        # Compara el resultado con el valor esperado para detectar un error en este requisito.
        self.assertEqual(r.context['tipo'], '')
        # Compara el resultado con el valor esperado para detectar un error en este requisito.
        self.assertEqual(r.context['pagina'].paginator.count, 2)

    # Crea más de diez coincidencias y comprueba navegación, filtros y páginas incorrectas.
    def test_paginacion_conserva_filtros(self):
        # Repite el caso para cada dato o ruta indicada, sin modificar la base real del proyecto.
        for i in range(11):
            # Añade un registro de contraste para comprobar que los filtros incluyen y excluyen correctamente.
            Contacto.objects.create(nombre=f'Club {i:02}', tipo='socio')
        # Agrupa los filtros que deben mantenerse al navegar entre páginas.
        datos = {'q': 'club', 'tipo': 'socio'}
        # Solicita la página y conserva la respuesta para comprobar su contenido y contexto.
        r = self.client.get(reverse('contactos:index'), datos)
        # Compara el resultado con el valor esperado para detectar un error en este requisito.
        self.assertEqual(len(r.context['objetos']), 10)
        # Verifica que el HTML contiene el dato esperado o que oculta una acción que ya no corresponde.
        self.assertContains(r, 'page=2&amp;q=club&amp;tipo=socio')
        # Solicita la página y conserva la respuesta para comprobar su contenido y contexto.
        r = self.client.get(reverse('contactos:index'), {**datos, 'page': 2})
        # Compara el resultado con el valor esperado para detectar un error en este requisito.
        self.assertEqual(len(r.context['objetos']), 2)
        # Compara el resultado con el valor esperado para detectar un error en este requisito.
        self.assertEqual(r.context['pagina'].number, 2)
        # Repite el caso para cada dato o ruta indicada, sin modificar la base real del proyecto.
        for pagina in ['abc', '999', '-1']:
            # Comprueba el estado HTTP esperado: 200 página, 302 redirección, 403 CSRF, 404 ausente o 405 método no permitido.
            self.assertEqual(self.client.get(reverse('contactos:index'), {'page': pagina}).status_code, 200)

    # Verifica el CSV completo, las tildes, las comillas y la protección frente a fórmulas.
    def test_csv_exporta_todas_las_paginas_y_escapa_texto(self):
        # Repite el caso para cada dato o ruta indicada, sin modificar la base real del proyecto.
        for i in range(12):
            # Añade un registro de contraste para comprobar que los filtros incluyen y excluyen correctamente.
            Contacto.objects.create(nombre=f'Exportación {i}', tipo='proveedor', notas='Pintura; "roja"\nSegunda línea')
        # Añade un registro de contraste para comprobar que los filtros incluyen y excluyen correctamente.
        Contacto.objects.create(nombre='=2+2', tipo='socio')
        # Solicita la página y conserva la respuesta para comprobar su contenido y contexto.
        r = self.client.get(reverse('contactos:exportar_csv'), {'tipo': 'proveedor', 'q': 'exportación', 'page': 2})
        # Compara el resultado con el valor esperado para detectar un error en este requisito.
        self.assertEqual(r['Content-Type'], 'text/csv; charset=utf-8')
        # Decodifica el CSV con su marca UTF-8 y vuelve a leer las filas usando punto y coma.
        filas = list(csv.reader(io.StringIO(r.content.decode('utf-8-sig')), delimiter=';'))
        # Compara el resultado con el valor esperado para detectar un error en este requisito.
        self.assertEqual(len(filas), 13)
        # Compara el resultado con el valor esperado para detectar un error en este requisito.
        self.assertEqual(filas[1][-1], 'Pintura; "roja"\nSegunda línea')
        # Solicita la página y conserva la respuesta para comprobar su contenido y contexto.
        r = self.client.get(reverse('contactos:exportar_csv'), {'q': '=2+2'})
        # Decodifica el CSV con su marca UTF-8 y vuelve a leer las filas usando punto y coma.
        filas = list(csv.reader(io.StringIO(r.content.decode('utf-8-sig')), delimiter=';'))
        # Compara el resultado con el valor esperado para detectar un error en este requisito.
        self.assertEqual(filas[1][0], "'=2+2")

    # Combina título/etapa y verifica qué ocurre sin coincidencias o con una etapa inválida.
    def test_filtro_oportunidades_y_limpieza(self):
        # Añade un registro de contraste para comprobar que los filtros incluyen y excluyen correctamente.
        Oportunidad.objects.create(titulo='Pedido miniaturas', contacto=self.socio, etapa='nuevo')
        # Añade un registro de contraste para comprobar que los filtros incluyen y excluyen correctamente.
        Oportunidad.objects.create(titulo='Torneo', contacto=self.socio, etapa='en_proceso')
        # Solicita la página y conserva la respuesta para comprobar su contenido y contexto.
        r = self.client.get(reverse('oportunidades:index'), {'q': 'pedido', 'etapa': 'en_proceso'})
        # Compara el resultado con el valor esperado para detectar un error en este requisito.
        self.assertEqual(list(r.context['objetos']), [self.op])
        # Verifica que el HTML contiene el dato esperado o que oculta una acción que ya no corresponde.
        self.assertContains(r, 'value="en_proceso" selected')
        # Compara el resultado con el valor esperado para detectar un error en este requisito.
        self.assertEqual(self.client.get(reverse('oportunidades:index'), {'etapa': 'incorrecta'}).context['objetos'].count(), 3)
        # Solicita la página y conserva la respuesta para comprobar su contenido y contexto.
        r = self.client.get(reverse('oportunidades:index'), {'q': 'zzz'})
        # Verifica que el HTML contiene el dato esperado o que oculta una acción que ya no corresponde.
        self.assertContains(r, 'No hay oportunidades que coincidan')

    # Exige POST y CSRF; ganar cambia la etapa, conserva el importe y devuelve a la ficha.
    def test_ganar_solo_post_y_csrf(self):
        # Construye la dirección de la acción a partir de su nombre y del identificador del registro.
        url = reverse('oportunidades:ganar', args=[self.op.pk])
        # Comprueba el estado HTTP esperado: 200 página, 302 redirección, 403 CSRF, 404 ausente o 405 método no permitido.
        self.assertEqual(self.client.get(url).status_code, 405)
        # Vuelve a leer la base de datos para comprobar el cambio guardado, no el objeto previo en memoria.
        self.op.refresh_from_db()
        # Compara el resultado con el valor esperado para detectar un error en este requisito.
        self.assertEqual(self.op.etapa, 'en_proceso')
        # Lee el token de la sesión de prueba para enviar un POST autorizado por CSRF.
        protegido = Client(enforce_csrf_checks=True)
        # Autentica al cliente de prueba para acceder a las vistas protegidas.
        protegido.force_login(self.usuario)
        # Comprueba el estado HTTP esperado: 200 página, 302 redirección, 403 CSRF, 404 ausente o 405 método no permitido.
        self.assertEqual(protegido.post(url).status_code, 403)
        # Solicita la página y conserva la respuesta para comprobar su contenido y contexto.
        r = protegido.get(reverse('oportunidades:detalle', args=[self.op.pk]))
        # Verifica que el HTML contiene el dato esperado o que oculta una acción que ya no corresponde.
        self.assertContains(r, 'Marcar como ganada')
        # Lee el token de la sesión de prueba para enviar un POST autorizado por CSRF.
        token = protegido.cookies['csrftoken'].value
        # Envía el formulario y conserva la respuesta para verificar el resultado del guardado.
        r = protegido.post(url, {'csrfmiddlewaretoken': token})
        # Comprueba que la acción redirige a la ficha de la oportunidad y que esa ficha carga.
        self.assertRedirects(r, reverse('oportunidades:detalle', args=[self.op.pk]))
        # Vuelve a leer la base de datos para comprobar el cambio guardado, no el objeto previo en memoria.
        self.op.refresh_from_db()
        # Compara el resultado con el valor esperado para detectar un error en este requisito.
        self.assertEqual(self.op.etapa, 'fidelizado')
        # Compara el resultado con el valor esperado para detectar un error en este requisito.
        self.assertEqual(self.op.importe, Decimal('125.50'))
        # Solicita la página y conserva la respuesta para comprobar su contenido y contexto.
        r = protegido.get(reverse('oportunidades:detalle', args=[self.op.pk]))
        # Verifica que el HTML contiene el dato esperado o que oculta una acción que ya no corresponde.
        self.assertNotContains(r, 'Marcar como ganada')
        # Comprueba el estado HTTP esperado: 200 página, 302 redirección, 403 CSRF, 404 ausente o 405 método no permitido.
        self.assertEqual(self.client.post(url).status_code, 302)  # Repetir es seguro.
        # Comprueba el estado HTTP esperado: 200 página, 302 redirección, 403 CSRF, 404 ausente o 405 método no permitido.
        self.assertEqual(self.client.post(reverse('oportunidades:ganar', args=[99999])).status_code, 404)

    # Distingue tareas vencidas, hechas, de hoy y futuras; comprueba también el total ganado.
    def test_panel_excluye_hechas_y_vencimiento_hoy(self):
        # Obtiene hoy en la zona del CRM para evitar depender de la fecha del equipo.
        hoy = timezone.localdate()
        # Añade un registro de contraste para comprobar que los filtros incluyen y excluyen correctamente.
        Tarea.objects.create(titulo='Vencida', vence=hoy - timedelta(days=1), prioridad='alta')
        # Añade un registro de contraste para comprobar que los filtros incluyen y excluyen correctamente.
        Tarea.objects.create(titulo='Hecha', vence=hoy - timedelta(days=1), hecha=True)
        # Añade un registro de contraste para comprobar que los filtros incluyen y excluyen correctamente.
        Tarea.objects.create(titulo='Hoy', vence=hoy)
        # Añade un registro de contraste para comprobar que los filtros incluyen y excluyen correctamente.
        Tarea.objects.create(titulo='Futura', vence=hoy + timedelta(days=1))
        # Fija la etapa necesaria para comprobar la suma del panel o la conversión de datos antiguos.
        self.op.etapa = 'fidelizado'
        # Guarda la etapa preparada para que la siguiente petición lea el estado de este escenario.
        self.op.save()
        # Solicita la página y conserva la respuesta para comprobar su contenido y contexto.
        r = self.client.get(reverse('inicio'))
        # Compara el resultado con el valor esperado para detectar un error en este requisito.
        self.assertEqual(r.context['vencidas'], 1)
        # Compara el resultado con el valor esperado para detectar un error en este requisito.
        self.assertEqual(r.context['pendientes'], 3)
        # Compara el resultado con el valor esperado para detectar un error en este requisito.
        self.assertEqual(r.context['fidelizado'], Decimal('125.50'))
        # Verifica que el HTML contiene el dato esperado o que oculta una acción que ya no corresponde.
        self.assertContains(r, '125,50')
        # Verifica que el HTML contiene el dato esperado o que oculta una acción que ya no corresponde.
        self.assertContains(r, 'Tareas pendientes vencidas')

    # Prueba crear, consultar, editar y borrar tareas; verifica campos propios y autor de interacciones.
    def test_formularios_y_crud(self):
        # Compara el resultado con el valor esperado para detectar un error en este requisito.
        self.assertIn('prioridad', TareaForm().fields)
        # Compara el resultado con el valor esperado para detectar un error en este requisito.
        self.assertIn('cuota_mensual', ContactoForm().fields)
        # Compara el resultado con el valor esperado para detectar un error en este requisito.
        self.assertIn('sistema_preferido', ContactoForm().fields)
        # Obtiene hoy en la zona del CRM para evitar depender de la fecha del equipo.
        hoy = timezone.localdate().isoformat()
        # Envía el formulario y conserva la respuesta para verificar el resultado del guardado.
        r = self.client.post(reverse('tareas:crear'), {'titulo': 'Organizar torneo', 'vence': hoy, 'prioridad': 'alta'})
        # Comprueba el estado HTTP esperado: 200 página, 302 redirección, 403 CSRF, 404 ausente o 405 método no permitido.
        self.assertEqual(r.status_code, 302)
        # Recupera el registro guardado para comprobar sus valores reales en la base temporal.
        tarea = Tarea.objects.get(titulo='Organizar torneo')
        # Compara el resultado con el valor esperado para detectar un error en este requisito.
        self.assertEqual(tarea.prioridad, 'alta')
        # Verifica que el HTML contiene el dato esperado o que oculta una acción que ya no corresponde.
        self.assertContains(self.client.get(reverse('tareas:index')), 'Alta')
        # Envía el formulario y conserva la respuesta para verificar el resultado del guardado.
        r = self.client.post(reverse('tareas:editar', args=[tarea.pk]), {'titulo': 'Organizar torneo', 'vence': hoy, 'prioridad': 'baja'})
        # Comprueba el estado HTTP esperado: 200 página, 302 redirección, 403 CSRF, 404 ausente o 405 método no permitido.
        self.assertEqual(r.status_code, 302)
        # Vuelve a leer la base de datos para comprobar el cambio guardado, no el objeto previo en memoria.
        tarea.refresh_from_db()
        # Compara el resultado con el valor esperado para detectar un error en este requisito.
        self.assertEqual(tarea.prioridad, 'baja')
        # Envía un formulario contra la base temporal para comprobar que la vista guarda o elimina el registro.
        self.client.post(reverse('tareas:borrar', args=[tarea.pk]))
        # Compara el resultado con el valor esperado para detectar un error en este requisito.
        self.assertFalse(Tarea.objects.filter(pk=tarea.pk).exists())
        # Envía un formulario contra la base temporal para comprobar que la vista guarda o elimina el registro.
        self.client.post(reverse('contactos:crear'), {'nombre': 'Pintora nueva', 'tipo': 'modelista', 'sistema_preferido': 'Legion', 'cuota_mensual': 'on'})
        # Recupera el registro guardado para comprobar sus valores reales en la base temporal.
        contacto = Contacto.objects.get(nombre='Pintora nueva')
        # Compara el resultado con el valor esperado para detectar un error en este requisito.
        self.assertTrue(contacto.cuota_mensual)
        # Verifica que el HTML contiene el dato esperado o que oculta una acción que ya no corresponde.
        self.assertContains(self.client.get(reverse('contactos:detalle', args=[contacto.pk])), 'Legion')
        # Envía un formulario contra la base temporal para comprobar que la vista guarda o elimina el registro.
        self.client.post(reverse('interacciones:crear'), {'contacto': contacto.pk, 'canal': 'whatsapp', 'resumen': 'Reserva confirmada'})
        # Compara el resultado con el valor esperado para detectar un error en este requisito.
        self.assertEqual(Interaccion.objects.get().autor, self.usuario)

    # Comprueba que los listados y los formularios de los cuatro módulos se pueden mostrar.
    def test_listados_y_formularios_cargan(self):
        # Repite el caso para cada dato o ruta indicada, sin modificar la base real del proyecto.
        for ns in ['contactos', 'oportunidades', 'interacciones', 'tareas']:
            # Repite el caso para cada dato o ruta indicada, sin modificar la base real del proyecto.
            for accion in ['index', 'crear']:
                # Comprueba el estado HTTP esperado: 200 página, 302 redirección, 403 CSRF, 404 ausente o 405 método no permitido.
                self.assertEqual(self.client.get(reverse(f'{ns}:{accion}')).status_code, 200)

    # Sin sesión, tanto las consultas como la acción de ganar deben redirigir al inicio de sesión.
    def test_rutas_protegidas(self):
        # Cierra la sesión del cliente para comprobar el acceso anónimo.
        self.client.logout()
        # Repite el caso para cada dato o ruta indicada, sin modificar la base real del proyecto.
        for nombre in ['contactos:index', 'contactos:exportar_csv', 'oportunidades:index']:
            # Comprueba el estado HTTP esperado: 200 página, 302 redirección, 403 CSRF, 404 ausente o 405 método no permitido.
            self.assertEqual(self.client.get(reverse(nombre)).status_code, 302)
        # Comprueba el estado HTTP esperado: 200 página, 302 redirección, 403 CSRF, 404 ausente o 405 método no permitido.
        self.assertEqual(self.client.post(reverse('oportunidades:ganar', args=[self.op.pk])).status_code, 302)

    # Simula datos de la plantilla y comprueba su conversión a las etapas actuales.
    def test_normaliza_etapas_antiguas(self):
        # Fija la etapa necesaria para comprobar la suma del panel o la conversión de datos antiguos.
        self.op.etapa = 'ganado'
        # Guarda la etapa preparada para que la siguiente petición lea el estado de este escenario.
        self.op.save()
        # Crea datos aislados con los campos necesarios para este caso de prueba.
        otra = Oportunidad.objects.create(titulo='Reserva antigua', contacto=self.socio, etapa='negociacion')
        # Carga la función de migración que debe adaptar los valores antiguos.
        migracion = import_module('oportunidades.migrations.0003_normalizar_etapas')
        # No modifica el esquema: solo necesita la conexión para actualizar datos.
        # Ejecuta la transformación de datos con el registro de modelos y la conexión temporal.
        migracion.normalizar_etapas(apps, connection.schema_editor())
        # Vuelve a leer la base de datos para comprobar el cambio guardado, no el objeto previo en memoria.
        self.op.refresh_from_db()
        # Vuelve a leer la base de datos para comprobar el cambio guardado, no el objeto previo en memoria.
        otra.refresh_from_db()
        # Compara el resultado con el valor esperado para detectar un error en este requisito.
        self.assertEqual(self.op.etapa, 'fidelizado')
        # Compara el resultado con el valor esperado para detectar un error en este requisito.
        self.assertEqual(otra.etapa, 'en_proceso')


# Agrupa la comprobación de los datos iniciales que recibirá el profesor.
class DatosEjemploTests(TestCase):
    # Carga ejemplos desde cero, valida todos los modelos y comprueba que repetir no duplica datos.
    def test_carga_limpia_coherente_y_repetible(self):
        # Ejecuta la carga de ejemplos y recoge sus mensajes sin imprimirlos durante las pruebas.
        call_command('cargar_ejemplo', stdout=io.StringIO())
        # Compara el resultado con el valor esperado para detectar un error en este requisito.
        self.assertEqual(Contacto.objects.count(), 8)
        # Compara el resultado con el valor esperado para detectar un error en este requisito.
        self.assertTrue(User.objects.get(username='admin').check_password('admin1234'))
        # full_clean detecta opciones que no pertenecen a los choices del modelo.
        # Repite el caso para cada dato o ruta indicada, sin modificar la base real del proyecto.
        for modelo in [Contacto, Oportunidad, Interaccion, Tarea]:
            # Repite el caso para cada dato o ruta indicada, sin modificar la base real del proyecto.
            for objeto in modelo.objects.all():
                # Valida campos y choices del modelo, no solo que SQLite acepte guardar el registro.
                objeto.full_clean()
        # Guarda los recuentos iniciales para detectar duplicados al cargar los ejemplos otra vez.
        cantidades = [modelo.objects.count() for modelo in [Contacto, Oportunidad, Interaccion, Tarea]]
        # Ejecuta la carga de ejemplos y recoge sus mensajes sin imprimirlos durante las pruebas.
        call_command('cargar_ejemplo', stdout=io.StringIO())
        # Compara el resultado con el valor esperado para detectar un error en este requisito.
        self.assertEqual(cantidades, [modelo.objects.count() for modelo in [Contacto, Oportunidad, Interaccion, Tarea]])
