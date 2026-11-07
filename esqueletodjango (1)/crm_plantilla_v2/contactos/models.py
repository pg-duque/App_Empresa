"""
MODELOS de Contactos. Un modelo = una tabla; cada atributo = una columna.
Tras CUALQUIER cambio aquí ejecuta:
    python manage.py makemigrations     # prepara los cambios
    python manage.py migrate            # los aplica a la base de datos
(Si usas iniciar.sh / iniciar.bat, se hace solo al arrancar.)
"""
from django.db import models


class Contacto(models.Model):
    # TODO-ALUMNO 1 completado: tipos adaptados a la comunidad de Modelmakers.
    # Cada pareja contiene el valor guardado en la base de datos y su etiqueta visible.
    TIPOS = [
        ('socio', 'Socio'),  # Miembro inscrito que puede pagar la cuota del club.
        ('jugador', 'Jugador Habitual'),  # Persona que participa o reserva partidas.
        ('modelista','Pintor / Modelista'),  # Contacto dedicado al montaje o pintura de miniaturas.
        ('proveedor', 'Proveedor / Marca'),  # Empresa o marca que suministra material.
        ('cliente', 'Cliente casual'),  # Comprador ocasional de la tienda.
        ('mesa', "Mesa de juego"),  # Recurso del club registrado para organizar sus reservas.
        ('otro','Otro')  # Alternativa para contactos que no encajan en los tipos anteriores.
    ]

    nombre = models.CharField(max_length=120)                        # Texto corto. max_length es OBLIGATORIO
    tipo = models.CharField(max_length=20, choices=TIPOS, default='cliente')  # choices -> desplegable en formularios
    email = models.EmailField(blank=True)                            # blank=True -> se puede dejar vacío
    telefono = models.CharField(max_length=30, blank=True)           # Teléfono como texto (admite +34, espacios)
    # El formulario valida un máximo de 500 caracteres; blank permite dejar las notas vacías.
    notas = models.TextField(blank=True, max_length=500)             # Texto largo
    creado = models.DateTimeField(auto_now_add=True)                 # auto_now_add -> fecha de creación automática
    # TODO-ALUMNO 2 completado: estado del pago mensual, no una cantidad de dinero.
    # default=False inicia la cuota sin pagar; verbose_name y help_text explican la casilla.
    cuota_mensual = models.BooleanField(default=False, verbose_name="Cuota mensual", help_text="Marca si el socio ha pagado la mensualidad de la asociación")  # Booleano con etiqueta y ayuda
    # Segundo campo propio: juego o actividad preferida, hasta 100 caracteres y opcional.
    # La etiqueta y el texto de ayuda se reutilizan al generar los formularios.
    sistema_preferido = models.CharField(max_length=100, blank=True, verbose_name="Sistema de juego preferido", help_text="P.ej. Warhammer 40k, Age of Sigmar, Star Wars X-Wing, etc.")  # Campo adicional para el sistema de juego preferido
    # Ambos campos están integrados en forms.py, admin.py, lista.html y la ficha de contacto.
    # Las migraciones 0002 y 0003 conservan estos cambios para crear una base desde cero.

    class Meta:
        ordering = ['nombre']              # Orden por defecto. '-campo' = descendente

    def __str__(self):
        return self.nombre                 # Cómo se muestra el objeto en admin, desplegables, títulos


# ---------------------------------------------------------------------------
# CATÁLOGO DE CAMPOS (referencia; todo comentado)
# CharField(max_length=N) texto corto | TextField() texto largo | EmailField() | URLField()
# IntegerField() / PositiveIntegerField() enteros | FloatField() decimal aproximado (no para dinero)
# DecimalField(max_digits=10, decimal_places=2) dinero | BooleanField(default=False) sí/no
# DateField() fecha | DateTimeField() fecha y hora | ImageField(upload_to='fotos/') (necesita Pillow)
# Opciones: null=True (BD admite vacío) · blank=True (formulario admite vacío) · default=valor
#           unique=True (sin repetidos) · choices=[(valor, 'Texto')] · verbose_name='Etiqueta'
#           help_text='Ayuda' · auto_now_add=True (fecha al crear) · auto_now=True (fecha al guardar)
# Relaciones: ForeignKey(Modelo, on_delete=..., related_name='x') muchos-a-uno
#             ManyToManyField(Modelo, blank=True) muchos-a-muchos | OneToOneField(Modelo, on_delete=...) uno-a-uno
# on_delete: CASCADE | PROTECT | SET_NULL (con null=True) | SET_DEFAULT | DO_NOTHING
# ---------------------------------------------------------------------------
