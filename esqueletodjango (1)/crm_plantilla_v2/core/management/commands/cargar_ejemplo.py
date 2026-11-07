"""
Comando:  python manage.py cargar_ejemplo
Crea el usuario admin (clave admin1234) y datos de ejemplo para que el CRM no esté vacío.
Es seguro ejecutarlo varias veces: no duplica datos.
TODO-ALUMNO 10: cambia los datos de ejemplo por los de TU temática (y los campos si los cambias en models.py).
"""
from datetime import date, timedelta
from django.apps import apps
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Carga usuario admin y datos de ejemplo'

    def handle(self, *args, **opciones):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin1234')
            self.stdout.write('Usuario creado: admin / admin1234')
        try:
            Contacto = apps.get_model('contactos', 'Contacto')
        except LookupError:
            return
        if Contacto.objects.exists():
            self.stdout.write('Ya había datos; no se carga nada más.')
            return
        # TODO-ALUMNO 10: ocho contactos del club; cuota_mensual indica si han pagado.
        # sistema_preferido guarda el juego o actividad asociado a cada contacto.
        # Cliente aficionado a X-Wing; incluye estado de cuota y sistema preferido.
        c1 = Contacto.objects.create(nombre='Paco García', tipo='cliente', email='paco@example.com', telefono='600111222', notas='Cliente habitual, le gusta el sistema X-Wing.', creado=date.today() - timedelta(days=30), cuota_mensual=True, sistema_preferido='X-Wing')
        # Socia del club con Warhammer 40k como sistema preferido.
        c2 = Contacto.objects.create(nombre='María López', tipo='socio', email='maria@example.com', telefono='600555666', notas='Socio desde 2023', creado=date.today() - timedelta(days=60), cuota_mensual=False, sistema_preferido='Warhammer 40k')
        # Proveedor de pinturas y herramientas para modelismo.
        c3 = Contacto.objects.create(nombre='Vallejo Modelismo', tipo='proveedor', email='info@vallejo.example.com', telefono='600777888', notas='Proveedor de pinturas y materiales de modelismo.', creado=date.today() - timedelta(days=90), cuota_mensual=False, sistema_preferido='Modelismo')
        # Primera mesa del club, registrada para seguir sus reservas de rol.
        c4 = Contacto.objects.create(nombre='Mesa de juego 1', tipo='mesa', email='', telefono='', notas='Mesa reservada para partidas de rol los viernes.', creado=date.today() - timedelta(days=15), cuota_mensual=False, sistema_preferido='Rol')
        # Jugador habitual de BattleTech que participa en las actividades.
        c5 = Contacto.objects.create(nombre='Juan Pérez', tipo='jugador', email='juan@example.com', telefono='600999000', notas='Jugador activo, le gusta el sistema BattleTech.', creado=date.today() - timedelta(days=10), cuota_mensual=False, sistema_preferido='BattleTech')
        # Segundo proveedor, especializado en pinturas para miniaturas.
        c6 = Contacto.objects.create(nombre='Warpaints', tipo='proveedor', email='info@warpaints.example.com', telefono='600123456', notas='Proveedor de pinturas para miniaturas.', creado=date.today() - timedelta(days=45), cuota_mensual=False, sistema_preferido='Modelismo')
        # Segunda mesa disponible para organizar partidas de wargames.
        c7 = Contacto.objects.create(nombre='Mesa de juego 2', tipo='mesa', email='', telefono='', notas='Mesa reservada para partidas de wargames los sábados.', creado=date.today() - timedelta(days=20), cuota_mensual=False, sistema_preferido='Wargames_Generico')
        # Pintora y modelista independiente que forma parte de la comunidad.
        c8 = Contacto.objects.create(nombre='Ana Torres', tipo='modelista', email='ana@example.com', telefono='600888999', notas='Modelista freelance, especializada en bustos.', creado=date.today() - timedelta(days=5), cuota_mensual=False, sistema_preferido='Modelismo')
        try:
            Op = apps.get_model('oportunidades', 'Oportunidad')
            # Las etapas coinciden con ETAPAS: en_proceso sustituye negociacion.
            # fidelizado representa ganado; los títulos corresponden a pedidos y reservas.
            # Oportunidad de ejemplo: Abono anual de mesas de X-Wing; empieza en la etapa en_proceso.
            Op.objects.create(titulo='Abono anual de mesas de X-Wing', contacto=c1, etapa='en_proceso', importe=1200, cierre_previsto=date.today() + timedelta(days=30))
            # Oportunidad de ejemplo: Pedido de miniaturas para socio; empieza en la etapa fidelizado.
            Op.objects.create(titulo='Pedido de miniaturas para socio', contacto=c2, etapa='fidelizado', importe=450)
            # Oportunidad de ejemplo: Presupuesto material; empieza en la etapa nuevo.
            Op.objects.create(titulo='Presupuesto material', contacto=c3, etapa='nuevo', importe=300)
            # Oportunidad de ejemplo: Reserva de mesa; empieza en la etapa perdido.
            Op.objects.create(titulo='Reserva de mesa', contacto=c4, etapa='perdido', importe=0)
            # Oportunidad de ejemplo: Suscripción mensual; empieza en la etapa en_proceso.
            Op.objects.create(titulo='Suscripción mensual', contacto=c5, etapa='en_proceso', importe=50, cierre_previsto=date.today() + timedelta(days=15))
            # Oportunidad de ejemplo: Consulta técnica; empieza en la etapa nuevo.
            Op.objects.create(titulo='Consulta técnica', contacto=c6, etapa='nuevo', importe=100)
            # Oportunidad de ejemplo: Torneo de wargames del club; empieza en la etapa en_proceso.
            Op.objects.create(titulo='Torneo de wargames del club', contacto=c7, etapa='en_proceso', importe=200, cierre_previsto=date.today() + timedelta(days=10))
            # Oportunidad de ejemplo: Solicitud de información; empieza en la etapa nuevo.
            Op.objects.create(titulo='Solicitud de información', contacto=c8, etapa='nuevo', importe=0)
        except LookupError:
            pass
        try:
            Inter = apps.get_model('interacciones', 'Interaccion')
            admin = User.objects.get(username='admin')
            # Historial por llamada: Primera llamada de presentación; el autor es el usuario de ejemplo.
            Inter.objects.create(contacto=c1, canal='llamada', resumen='Primera llamada de presentación', autor=admin)
            # Historial por email: Enviado presupuesto; el autor es el usuario de ejemplo.
            Inter.objects.create(contacto=c1, canal='email', resumen='Enviado presupuesto', autor=admin)
            # Historial por reunion: Reunión en oficina; el autor es el usuario de ejemplo.
            Inter.objects.create(contacto=c2, canal='reunion', resumen='Reunión en oficina', autor=admin)
            # Historial por nota: Cliente interesado en productos de modelismo; el autor es el usuario de ejemplo.
            Inter.objects.create(contacto=c3, canal='nota', resumen='Cliente interesado en productos de modelismo', autor=admin)
            # Historial por whatsapp: Confirmada reserva de mesa para el viernes; el autor es el usuario de ejemplo.
            Inter.objects.create(contacto=c4, canal='whatsapp', resumen='Confirmada reserva de mesa para el viernes', autor=admin)
            # Historial por llamada: Llamada para confirmar asistencia a torneo; el autor es el usuario de ejemplo.
            Inter.objects.create(contacto=c5, canal='llamada', resumen='Llamada para confirmar asistencia a torneo', autor=admin)
            # Historial por email: Enviado catálogo de pinturas; el autor es el usuario de ejemplo.
            Inter.objects.create(contacto=c6, canal='email', resumen='Enviado catálogo de pinturas', autor=admin)
            # Historial por reunion: Reunión para discutir reglas del torneo; el autor es el usuario de ejemplo.
            Inter.objects.create(contacto=c7, canal='reunion', resumen='Reunión para discutir reglas del torneo', autor=admin)
            # Historial por nota: Modelista solicita información sobre técnicas de pintura; el autor es el usuario de ejemplo.
            Inter.objects.create(contacto=c8, canal='nota', resumen='Modelista solicita información sobre técnicas de pintura', autor=admin)
        except LookupError:
            pass
        try:
            Tarea = apps.get_model('tareas', 'Tarea')
            # TODO-ALUMNO 5: alta para la factura vencida, baja para reglas y media por defecto.
            # Seguimiento del club: Llamar para cerrar contrato; prioridad media (predeterminada).
            Tarea.objects.create(titulo='Llamar para cerrar contrato', contacto=c1, vence=date.today() + timedelta(days=3))
            # Seguimiento del club: Enviar factura; prioridad alta.
            Tarea.objects.create(titulo='Enviar factura', contacto=c2, vence=date.today() - timedelta(days=1), prioridad='alta')
            # Seguimiento del club: Preparar material para reunión; prioridad media (predeterminada).
            Tarea.objects.create(titulo='Preparar material para reunión', contacto=c3, vence=date.today() + timedelta(days=5))
            # Seguimiento del club: Confirmar asistencia al torneo; prioridad media (predeterminada).
            Tarea.objects.create(titulo='Confirmar asistencia al torneo', contacto=c5, vence=date.today() + timedelta(days=2))
            # Seguimiento del club: Revisar pedido de pinturas; prioridad media (predeterminada).
            Tarea.objects.create(titulo='Revisar pedido de pinturas', contacto=c6, vence=date.today() + timedelta(days=4))
            # Seguimiento del club: Actualizar reglas del torneo; prioridad baja.
            Tarea.objects.create(titulo='Actualizar reglas del torneo', contacto=c7, vence=date.today() + timedelta(days=7), prioridad='baja')
            # Seguimiento del club: Responder consulta de modelista; prioridad media (predeterminada).
            Tarea.objects.create(titulo='Responder consulta de modelista', contacto=c8, vence=date.today() + timedelta(days=1))
        except LookupError:
            pass
        self.stdout.write('Datos de ejemplo cargados.')
