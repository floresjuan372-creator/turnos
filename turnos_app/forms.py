from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import *



class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = [
            'dni',
            'fecha_nacimiento',
            'telefono',
        ]


class PacientePerfilForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['dni', 'fecha_nacimiento', 'telefono']
        widgets = {
            'fecha_nacimiento': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'}
            )
        }


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


class ProfesionalForm(forms.ModelForm):
    class Meta:
        model = Profesional
        fields = [
            'nombre',
            'apellido',
            'matricula',
            'especialidad',
            'email',
            'activo'
        ]

class registroform(UserCreationForm):
    email = forms.EmailField(label="Correo electrónico", required=True)
    first_name = forms.CharField(label="Nombre", max_length=30, required=True)
    last_name = forms.CharField(label="Apellido", max_length=30, required=True)

    
    dni = forms.CharField(label="DNI", max_length=20, required=True)
    fecha_nacimiento = forms.DateField(
        label="Fecha de nacimiento",
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True
    )
    telefono = forms.CharField(label="Teléfono", max_length=30, required=False)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
            'first_name',
            'last_name',
            'dni',
            'fecha_nacimiento',
            'telefono',
        ]
       

class profileform(UserChangeForm):
    email = forms.EmailField(label="Correo electronico", required=True)
    first_name = forms.CharField(label="Nombre", max_length=30, required=True)
    last_name = forms.CharField(label="Apellido", max_length=30, required=True)

    class Meta:
        model = User
        fields = ['email', "first_name", "last_name"]

class avatarform(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']