"""
FORMULARIOS: un ModelForm genera el formulario HTML a partir del modelo (con sus validaciones).
"""
from django import forms
from .models import Contacto


class ContactoForm(forms.ModelForm):
    class Meta:
        model = Contacto
        # fields = lista de campos que aparecen. Alternativas: '__all__' (todos) o exclude = [...]
        fields = ['nombre', 'tipo', 'email', 'telefono', 'notas', 'cuota_mesnual', 'sistema_preferido']
        widgets = {
            
            # widget = cómo se dibuja un campo: forms.Textarea(attrs={'rows': 3}) · forms.DateInput(attrs={'type': 'date'})
        }
