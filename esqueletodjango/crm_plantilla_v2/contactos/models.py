"""
MODELOS de Contactos. Un modelo = una tabla; cada atributo = una columna.
Tras CUALQUIER cambio aquí ejecuta:
    python manage.py makemigrations     # prepara los cambios
    python manage.py migrate            # los aplica a la base de datos
(Si usas iniciar.sh / iniciar.bat, se hace solo al arrancar.)
"""
from django.db import models


class Contacto(models.Model):
    # choices: lista de pares (valor_guardado_en_BD, texto_visible). Cámbialas por las de tu temática.
    TIPOS = [
        ('socio', 'Socio'),
        ('jugador', 'Jugador Habitual'),
        ('modelista','Pintor / Modelista'),
        ('proveedor', 'Proveedor / Marca'),
        ('cliente', 'Cliente casual'),
        ('mesa', "Mesa de juego"),
        ('otro','Otro')
        # TODO-ALUMNO 1: añade/renombra tipos (ej: 'socio', 'jugador', 'paciente', 'alumno'...)
    ]

    nombre = models.CharField(max_length=120)                        # Texto corto. max_length es OBLIGATORIO
    tipo = models.CharField(max_length=20, choices=TIPOS, default='cliente')  # choices -> desplegable en formularios
    email = models.EmailField(blank=True)                            # blank=True -> se puede dejar vacío
    telefono = models.CharField(max_length=30, blank=True)           # Teléfono como texto (admite +34, espacios)
    notas = models.TextField(blank=True, max_length=500)             # Texto largo
    creado = models.DateTimeField(auto_now_add=True)                 # auto_now_add -> fecha de creación automática
    cuota_mensual = models.BooleanField(default=False, verbose_name="Cuota mensual", help_text="Marca si el socio ha pagado la mensualidad de la asociación")  # Booleano con etiqueta y ayuda
    sistema_preferido = models.CharField(max_length=100, blank=True, verbose_name="Sistema de juego preferido", help_text="P.ej. Warhammer 40k, Age of Sigmar, Star Wars X-Wing, etc.")  # Campo adicional para el sistema de juego preferido
    # TODO-ALUMNO 2: añade 2 campos propios de tu temática (ver catálogo abajo). Después:
    #   python manage.py makemigrations && python manage.py migrate
    #   y añádelos a forms.py (fields), admin.py (list_display) y lista.html (columnas).

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
