"""Nivel 4: pruebas funcionales con una base temporal que no altera los datos reales."""
# Recoge los mensajes del comando de ejemplos en memoria.
import io
# Usuario de prueba para acceder a las vistas que exigen sesión.
from django.contrib.auth.models import User
# Permite invocar cargar_ejemplo igual que desde manage.py.
from django.core.management import call_command
# TestCase aísla datos; Client simula un navegador y puede exigir tokens CSRF.
from django.test import Client, TestCase
# Genera las rutas por nombre y obtiene la fecha según la zona horaria del CRM.
from django.urls import reverse
from django.utils import timezone
# Modelos utilizados para comprobar el vínculo con el organizador y los eventos.
from contactos.models import Contacto
from .models import Evento
# Formulario usado para verificar que la fecha se dibuja correctamente al editar.
from .forms import EventoForm


class EventosTests(TestCase):
    """Comprueba búsqueda, CRUD, validación, permisos y datos iniciales del módulo."""

    def setUp(self):
        # Prepara un usuario autenticado y un contacto organizador antes de cada caso.
        self.usuario = User.objects.create_user('organizador', password='prueba-eventos')
        self.client.force_login(self.usuario)
        self.contacto = Contacto.objects.create(nombre='Socia organizadora', tipo='socio')
        # Datos válidos para reutilizar en los formularios de alta y edición.
        self.datos = {'titulo': 'Taller del club', 'tipo': 'taller',
                      'fecha': timezone.localdate().isoformat(), 'lugar': 'Mesa de pintura',
                      'aforo': 8, 'contacto': self.contacto.pk, 'descripcion': 'Pinceles y luces'}
        # La base inicial contiene una actividad; el modelo recibe el Contacto, no su identificador de formulario.
        self.evento = Evento.objects.create(**{**self.datos, 'contacto': self.contacto})

    def test_integracion_menu_panel_contacto(self):
        # El menú y una tarjeta del panel deben ofrecer acceso a Eventos.
        respuesta = self.client.get(reverse('inicio'))
        self.assertContains(respuesta, reverse('eventos:index'))
        self.assertTrue(any(t['etiqueta'] == 'Eventos' and t['n'] == 1 for t in respuesta.context['resumen']))
        # La ficha del contacto muestra su actividad y permite precargarlo al crear otra.
        respuesta = self.client.get(reverse('contactos:detalle', args=[self.contacto.pk]))
        self.assertContains(respuesta, 'Taller del club')
        self.assertContains(respuesta, reverse('eventos:crear') + '?contacto=' + str(self.contacto.pk))

    def test_busqueda_ficha_y_sin_resultados(self):
        # Un segundo evento permite comprobar que la búsqueda excluye resultados distintos.
        Evento.objects.create(titulo='Torneo', fecha=timezone.localdate(), lugar='Sala')
        respuesta = self.client.get(reverse('eventos:index'), {'q': '  TALLER  '})
        self.assertEqual(list(respuesta.context['objetos']), [self.evento])
        self.assertContains(respuesta, 'Taller de pintura')
        # La ficha común debe presentar descripción y organizador del evento.
        respuesta = self.client.get(reverse('eventos:detalle', args=[self.evento.pk]))
        self.assertContains(respuesta, 'Pinceles y luces')
        self.assertContains(respuesta, 'Socia organizadora')
        # Las consultas sin coincidencias o con identificadores inexistentes tienen respuesta controlada.
        self.assertContains(self.client.get(reverse('eventos:index'), {'q': 'inexistente'}), 'No hay eventos')
        self.assertEqual(self.client.get(reverse('eventos:detalle', args=[99999])).status_code, 404)

    def test_crear_editar_y_calendario(self):
        # Crear desde una ficha de contacto precarga el organizador del formulario.
        respuesta = self.client.get(reverse('eventos:crear'), {'contacto': self.contacto.pk})
        self.assertEqual(str(respuesta.context['form'].initial['contacto']), str(self.contacto.pk))
        # La edición usa un calendario HTML con el valor de fecha en formato ISO.
        formulario = EventoForm(instance=self.evento)
        self.assertIn('type="date"', str(formulario['fecha']))
        self.assertIn(timezone.localdate().isoformat(), str(formulario['fecha']))
        # Un alta válida crea un registro y redirige a su ficha.
        respuesta = self.client.post(reverse('eventos:crear'), {**self.datos, 'titulo': 'Nuevo torneo'})
        creado = Evento.objects.get(titulo='Nuevo torneo')
        self.assertRedirects(respuesta, reverse('eventos:detalle', args=[creado.pk]))
        # La edición modifica ese registro y admite dejar el organizador vacío.
        respuesta = self.client.post(reverse('eventos:editar', args=[creado.pk]),
                                     {**self.datos, 'titulo': 'Torneo actualizado', 'aforo': 20, 'contacto': ''})
        self.assertRedirects(respuesta, reverse('eventos:detalle', args=[creado.pk]))
        creado.refresh_from_db()  # Lee los valores efectivamente guardados.
        self.assertEqual(creado.aforo, 20)
        self.assertEqual(creado.titulo, 'Torneo actualizado')
        self.assertIsNone(creado.contacto)
        self.assertEqual(Evento.objects.count(), 2)

    def test_datos_invalidos_no_crean_eventos(self):
        # Prueba límites del aforo, fecha, tipo, lugar, contacto y longitud de descripción.
        for cambios in [{'aforo': 0}, {'aforo': -1}, {'fecha': 'no-es-fecha'},
                        {'tipo': 'desconocido'}, {'lugar': ''}, {'contacto': 99999},
                        {'descripcion': 'x' * 1001}]:
            # Cada POST inválido debe volver al formulario con errores de validación.
            respuesta = self.client.post(reverse('eventos:crear'), {**self.datos, **cambios})
            self.assertEqual(respuesta.status_code, 200)
            self.assertTrue(respuesta.context['form'].errors)
        # No se guarda ninguno de los intentos anteriores.
        self.assertEqual(Evento.objects.count(), 1)

    def test_borrado_solo_post_con_csrf(self):
        # GET muestra la confirmación sin borrar el evento.
        url = reverse('eventos:borrar', args=[self.evento.pk])
        self.assertEqual(self.client.get(url).status_code, 200)
        self.assertTrue(Evento.objects.filter(pk=self.evento.pk).exists())
        # Este cliente exige CSRF para verificar el mismo comportamiento que un navegador.
        navegador = Client(enforce_csrf_checks=True)
        navegador.force_login(self.usuario)
        self.assertEqual(navegador.post(url).status_code, 403)
        # Obtiene el token del formulario y confirma el borrado con POST.
        navegador.get(url)
        respuesta = navegador.post(url, {'csrfmiddlewaretoken': navegador.cookies['csrftoken'].value})
        self.assertRedirects(respuesta, reverse('eventos:index'))
        self.assertFalse(Evento.objects.filter(pk=self.evento.pk).exists())

    def test_conservar_evento_al_borrar_organizador(self):
        # SET_NULL mantiene el evento cuando desaparece el contacto relacionado.
        self.contacto.delete()
        self.evento.refresh_from_db()
        self.assertIsNone(self.evento.contacto)
        self.assertContains(self.client.get(reverse('eventos:index')), 'Taller del club')

    def test_vistas_requieren_sesion(self):
        # Todas las consultas y modificaciones deben redirigir al login sin una sesión.
        self.client.logout()
        for accion in ['index', 'crear', 'detalle', 'editar', 'borrar']:
            # Solo las rutas de listado y alta se resuelven sin identificador.
            argumentos = [self.evento.pk] if accion in ['detalle', 'editar', 'borrar'] else []
            url = reverse('eventos:' + accion, args=argumentos)
            self.assertEqual(self.client.get(url).status_code, 302)
            self.assertEqual(self.client.post(url, self.datos).status_code, 302)

    def test_ejemplos_con_contactos_existentes_sin_duplicados(self):
        # Incluso con contactos previos, el comando añade cuatro actividades del club.
        call_command('cargar_ejemplo', stdout=io.StringIO())
        self.assertEqual(Evento.objects.count(), 5)
        # Simula una edición del alumno para comprobar que la segunda carga la conserva.
        ejemplo = Evento.objects.get(titulo='Torneo de Warhammer 40k')
        ejemplo.lugar = 'Sala cambiada por el usuario'
        ejemplo.save(update_fields=['lugar'])
        call_command('cargar_ejemplo', stdout=io.StringIO())
        ejemplo.refresh_from_db()
        self.assertEqual(ejemplo.lugar, 'Sala cambiada por el usuario')
        self.assertEqual(Evento.objects.count(), 5)
        # full_clean valida también los choices y el aforo de todos los ejemplos cargados.
        for evento in Evento.objects.all():
            evento.full_clean()
