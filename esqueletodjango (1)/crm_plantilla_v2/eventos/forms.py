"""Formulario del módulo de eventos, siguiendo el ModelForm de tareas."""
# forms genera controles HTML y valida los campos del modelo.
from django import forms
# Modelo cuyos campos se editan en este formulario.
from .models import Evento


class EventoForm(forms.ModelForm):
    class Meta:
        # Asocia el formulario a la tabla de eventos.
        model = Evento
        # Enumera los campos editables para que las altas y modificaciones sean explícitas.
        fields = ['titulo', 'tipo', 'fecha', 'lugar', 'aforo', 'contacto', 'descripcion']
        # Personaliza la fecha con un calendario y la descripción con un área de texto corta.
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }
