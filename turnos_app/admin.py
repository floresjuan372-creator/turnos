from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Especialidad)
admin.site.register(Profesional)    
admin.site.register(Paciente)
admin.site.register(Turno)
admin.site.register(Profile)

