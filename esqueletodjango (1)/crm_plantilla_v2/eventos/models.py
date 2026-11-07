"""Nivel 4: actividades de Modelmakers. Tras modificar campos, generar y aplicar migraciones."""
# models proporciona los campos de la tabla y las relaciones con contactos.
from django.db import models
# Impide guardar un aforo inferior a una persona desde los formularios.
from django.core.validators import MinValueValidator


class Evento(models.Model):
    # Cada pareja indica el valor guardado y la etiqueta visible en el desplegable.
    TIPOS = [
        ('torneo', 'Torneo'),  # Competición de wargames del club.
        ('taller', 'Taller de pintura'),  # Actividad guiada de pintura o modelismo.
        ('partida', 'Partida organizada'),  # Encuentro para jugar en las mesas del local.
        ('presentacion', 'Presentación'),  # Demostración de juegos, miniaturas o novedades.
    ]
    # Nombre del evento, obligatorio y limitado a 150 caracteres.
    titulo = models.CharField(max_length=150)
    # choices valida el tipo y genera sus etiquetas; comienza como partida organizada.
    tipo = models.CharField(max_length=20, choices=TIPOS, default='partida')
    # Fecha obligatoria; se admiten eventos pasados para conservar el historial del club.
    fecha = models.DateField()
    # Lugar o mesa donde se celebrará; debe introducirse al crear el evento.
    lugar = models.CharField(max_length=120)
    # Plazas disponibles: entero con mínimo 1; por defecto se ofrecen 12 plazas.
    aforo = models.PositiveIntegerField(default=12, validators=[MinValueValidator(1)])
    # Información adicional opcional con validación de hasta 1000 caracteres.
    descripcion = models.TextField(blank=True, max_length=1000, verbose_name='Descripción')
    # Contacto que organiza el evento, opcional; SET_NULL conserva el evento si se borra el contacto.
    contacto = models.ForeignKey(
        'contactos.Contacto', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='eventos', verbose_name='Organizador',  # contacto.eventos.all() consulta sus eventos.
    )

    class Meta:
        # Ordena por fecha y, si coinciden, por identificador para mantener un orden estable.
        ordering = ['fecha', 'id']

    def __str__(self):
        # Muestra el título en fichas, mensajes y desplegables del administrador.
        return self.titulo
