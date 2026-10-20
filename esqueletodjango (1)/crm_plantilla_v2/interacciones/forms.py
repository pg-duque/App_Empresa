"""
FORMULARIOS: un ModelForm crea un formulario a partir de un modelo
y aprovecha sus campos y validaciones.
"""

# Importa las herramientas para crear formularios de Django.
from django import forms

# Importa el modelo Interaccion, cuyos datos tendrá el formulario.
from .models import Interaccion


# Crea un formulario basado en el modelo Interaccion.
class InteraccionForm(forms.ModelForm):

    # Clase especial donde se configura este ModelForm.
    class Meta:

        # Indica qué modelo se usará para crear el formulario.
        model = Interaccion

        # Indica qué campos del modelo aparecerán en el formulario.
        # También podrías usar '__all__' para incluirlos todos,
        # o exclude = ['campo'] para dejar fuera alguno.
        fields = ['contacto', 'canal', 'resumen']

        # Permite personalizar cómo se dibuja cada campo en el HTML.
        # Por ahora está vacío, así que Django usará los widgets predeterminados.
        widgets = {
            # Ejemplo: forms.Textarea(attrs={'rows': 3})
            # mostraría el campo como un cuadro de texto de varias líneas.

            # Ejemplo: forms.DateInput(attrs={'type': 'date'})
            # mostraría el campo como un selector de fecha.
        }
