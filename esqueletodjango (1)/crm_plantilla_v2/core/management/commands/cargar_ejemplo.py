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
        c1 = Contacto.objects.create(nombre='Ana García', tipo='cliente', email='ana@example.com', telefono='600111222', notas='Cliente desde 2024')
        c2 = Contacto.objects.create(nombre='Luis Pérez', tipo='cliente', email='luis@example.com', telefono='600333444')
        c3 = Contacto.objects.create(nombre='Suministros SL', tipo='proveedor', email='info@suministros.example')
        try:
            Op = apps.get_model('oportunidades', 'Oportunidad')
            Op.objects.create(titulo='Contrato anual', contacto=c1, etapa='negociacion', importe=1200, cierre_previsto=date.today() + timedelta(days=30))
            Op.objects.create(titulo='Pedido inicial', contacto=c2, etapa='ganado', importe=450)
            Op.objects.create(titulo='Presupuesto material', contacto=c3, etapa='nuevo', importe=300)
        except LookupError:
            pass
        try:
            Inter = apps.get_model('interacciones', 'Interaccion')
            admin = User.objects.get(username='admin')
            Inter.objects.create(contacto=c1, canal='llamada', resumen='Primera llamada de presentación', autor=admin)
            Inter.objects.create(contacto=c1, canal='email', resumen='Enviado presupuesto', autor=admin)
            Inter.objects.create(contacto=c2, canal='reunion', resumen='Reunión en oficina', autor=admin)
        except LookupError:
            pass
        try:
            Tarea = apps.get_model('tareas', 'Tarea')
            Tarea.objects.create(titulo='Llamar para cerrar contrato', contacto=c1, vence=date.today() + timedelta(days=3))
            Tarea.objects.create(titulo='Enviar factura', contacto=c2, vence=date.today() - timedelta(days=1))
        except LookupError:
            pass
        self.stdout.write('Datos de ejemplo cargados.')
