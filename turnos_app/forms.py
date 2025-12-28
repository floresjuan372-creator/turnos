from django import forms
from .models import *


class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = [
            'nombre',
            'apellido',
            'dni',
            'fecha_nacimiento',
            'telefono',
            'email'
        ]


class TurnoForm(forms.ModelForm):

    class Meta:
        model = Turno
        fields = [
            'paciente',
            'profesional',
            'fecha',
            'hora'
        ]
        widgets = {
            'fecha': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'}
            ),
            'hora': forms.TimeInput(
                attrs={'type': 'time', 'class': 'form-control'}
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        profesional = cleaned_data.get('profesional')
        fecha = cleaned_data.get('fecha')
        hora = cleaned_data.get('hora')

        if profesional and fecha and hora:
            existe = Turno.objects.filter(
                profesional=profesional,
                fecha=fecha,
                hora=hora
            ).exists()

            if existe:
                raise forms.ValidationError(
                    "El profesional ya tiene un turno en ese horario."
                )

        return cleaned_data