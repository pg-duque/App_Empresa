"""
MODELOS de Tareas. Un modelo representa una tabla de la base de datos;
cada campo del modelo representa una columna.
Tras cambiar el modelo, ejecuta:
    python manage.py makemigrations  # Prepara una migración con los cambios.
    python manage.py migrate         # Aplica los cambios a la base de datos.
(Si usas iniciar.sh / iniciar.bat, estos comandos se ejecutan al arrancar.)
"""

# Importa las herramientas para definir modelos y campos de base de datos.
from django.db import models


# Define el modelo Tarea.
class Tarea(models.Model):

    # Campo de texto para el título. Acepta hasta 150 caracteres.
    titulo = models.CharField(max_length=150)

    # Relaciona la tarea con un contacto.
    # 'contactos.Contacto' indica la app y el modelo relacionado.
    # CASCADE significa que, al borrar el contacto, también se borran sus tareas.
    # null=True permite que la base de datos guarde la tarea sin contacto.
    # blank=True permite dejar el campo vacío en los formularios.
    # related_name permite obtener las tareas de un contacto con:
    # contacto.tareas.all()
    contacto = models.ForeignKey(
        'contactos.Contacto',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='tareas'
    )

    # Guarda la fecha límite de la tarea, sin incluir la hora.
    # Es obligatorio porque no se permite dejarlo vacío.
    vence = models.DateField()

    # Campo verdadero/falso, que normalmente se muestra como una casilla.
    # Las tareas nuevas empiezan como pendientes (hecha=False).
    hecha = models.BooleanField(default=False)

    # TODO-ALUMNO 5: añade un campo llamado prioridad con opciones alta, media y baja.
    # Puedes usar choices para limitar los valores permitidos.

    # Configuración adicional del modelo.
    class Meta:

        # Ordena primero por "hecha" y después por "vence".
        # Como False va antes que True, las pendientes aparecen primero;
        # dentro de cada grupo, se ordenan por fecha límite.
        ordering = ['hecha', 'vence']

    # Indica cómo se muestra una tarea como texto, por ejemplo en el administrador.
    # En este caso, se muestra su título.
    def __str__(self):
        return self.titulo
