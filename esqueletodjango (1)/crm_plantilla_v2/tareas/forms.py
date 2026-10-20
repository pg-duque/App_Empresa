"""
FORMULARIOS: un ModelForm crea un formulario a partir de un modelo
y aprovecha sus campos y validaciones.
"""

# Importa las herramientas para crear formularios de Django.
from django import forms

# Importa el modelo Tarea, cuyos datos tendrá el formulario.
from .models import Tarea


# Crea un formulario basado en el modelo Tarea.
class TareaForm(forms.ModelForm):

    # Clase especial donde se configura este ModelForm.
    class Meta:

        # Indica qué modelo se usará para crear el formulario.
        model = Tarea

        # Indica qué campos del modelo aparecerán.
        # También podrías usar '__all__' para incluirlos todos,
        # o exclude = ['campo'] para dejar fuera alguno.
        fields = ['titulo', 'contacto', 'vence', 'hecha']

        # Personaliza cómo se dibujan ciertos campos en el HTML.
        widgets = {
            # Muestra "vence" como selector de fecha del navegador.
            # format indica el formato de fecha esperado: año-mes-día.
            'vence': forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d'
            ),

            # Otros ejemplos de widgets:
            # forms.Textarea(attrs={'rows': 3}) muestra un cuadro de texto de varias líneas.
            # forms.DateInput(attrs={'type': 'date'}) muestra un selector de fecha.
        }
