# Importa las herramientas para crear formularios de Django.
from django import forms

# Importa el modelo Oportunidad, que define los datos que se guardan en la base de datos.
from .models import Oportunidad


# Crea un formulario basado en el modelo Oportunidad.
# Django genera los campos HTML y reutiliza las validaciones del modelo.
class OportunidadForm(forms.ModelForm):

    # Meta es una clase especial donde se configura el ModelForm.
    class Meta:

        # Indica qué modelo se usará como base para crear el formulario.
        model = Oportunidad

        # Lista los campos del modelo que aparecerán en el formulario.
        # Si quisieras mostrar todos, podrías usar fields = '__all__'.
        # Otra opción es excluir algunos con exclude = ['nombre_del_campo'].
        fields = ['titulo', 'contacto', 'etapa', 'importe', 'cierre_previsto']

        # Permite personalizar cómo se verá cada campo en el HTML.
        widgets = {
            # Muestra cierre_previsto como un selector de fecha del navegador.
            # format indica el formato de fecha que el formulario espera: año-mes-día.
            'cierre_previsto': forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d'
            ),
        }
