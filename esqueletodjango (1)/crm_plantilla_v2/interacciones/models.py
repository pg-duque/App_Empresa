"""
MODELOS de Interacciones. Un modelo representa una tabla de la base de datos;
cada campo del modelo representa una columna.
Tras cambiar el modelo, ejecuta:
    python manage.py makemigrations  # Prepara una migración con los cambios.
    python manage.py migrate         # Aplica los cambios a la base de datos.
(Si usas iniciar.sh / iniciar.bat, estos comandos se ejecutan al arrancar.)
"""

# Importa las herramientas para definir modelos y campos de base de datos.
from django.db import models

# Importa la hora y fecha actuales con la zona horaria configurada en Django.
from django.utils import timezone


# Define el modelo Interaccion.
class Interaccion(models.Model):

    # Opciones posibles para el campo "canal".
    # En cada pareja, el primer valor se guarda en la base de datos;
    # el segundo es el texto que se muestra en pantalla.
    CANALES = [
        ('llamada', 'Llamada'),
        ('email', 'Email'),
        ('reunion', 'Reunión'),
        ('nota', 'Nota'),
        # TODO-ALUMNO 4: añade otro canal, por ejemplo ('whatsapp', 'WhatsApp').
    ]

    # Relaciona cada interacción con un contacto.
    # 'contactos.Contacto' indica la app y el modelo relacionado.
    # CASCADE significa que, si se borra el contacto, también se borran
    # sus interacciones.
    # related_name permite consultar las interacciones desde un contacto:
    # contacto.interacciones.all()
    contacto = models.ForeignKey(
        'contactos.Contacto',
        on_delete=models.CASCADE,
        related_name='interacciones'
    )

    # Guarda el canal usado, limitado a las opciones de CANALES.
    # Si no se especifica, se elige 'nota'.
    canal = models.CharField(
        max_length=20,
        choices=CANALES,
        default='nota'
    )

    # Guarda el resumen de la interacción.
    # TextField permite texto largo, sin un límite pequeño de caracteres.
    resumen = models.TextField()

    # Guarda la fecha y la hora de la interacción.
    # timezone.now se pasa sin paréntesis para que Django la ejecute
    # al crear cada interacción y use la hora actual en ese momento.
    fecha = models.DateTimeField(default=timezone.now)

    # Relaciona la interacción con un usuario de Django.
    # SET_NULL conserva la interacción y deja autor vacío si se borra el usuario.
    # Para que eso sea posible, null=True permite guardar NULL en la base de datos
    # y blank=True permite dejar el campo vacío en formularios.
    # 'auth.User' se refiere al modelo de usuarios de Django.
    autor = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    # Configuración adicional del modelo.
    class Meta:

        # Ordena por fecha de más reciente a más antigua.
        # El signo menos delante de fecha indica orden descendente.
        ordering = ['-fecha']

        # Nombre plural que Django muestra para este modelo en el administrador.
        verbose_name_plural = 'interacciones'

    # Define cómo se representa una interacción como texto.
    def __str__(self):

        # get_canal_display() devuelve el texto legible de la opción elegida
        # (por ejemplo, 'Llamada' en vez de 'llamada').
        # {self.contacto} añade el contacto relacionado.
        return f'{self.get_canal_display()} con {self.contacto}'
