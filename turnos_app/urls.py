from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', inicio, name='inicio'),  # Ruta raíz redirige al admin
    path('turnos/', turnos, name='turnos'),
    path('crear_turno/', crear_turno, name='crear_turno'),
    path('turnoUpdate/<int:id>/', turnoUpdate, name='turnoUpdate'),
    path('turnoDelete/<int:id>/', turnoDelete, name='turnoDelete'),
    path('profesionales/', profesionales, name='profesionales'),
    path('pacientes/', pacientes, name='pacientes'),
    path('lista_pacientes/', lista_pacientes, name='lista_pacientes'),
    path('crear_paciente/', crear_paciente, name='crear_paciente'),
    path('pacienteUpdate/<int:id>/', pacienteUpdate, name='paciente_update'),
    path('pacienteDelete/<int:id>/', pacienteDelete, name='paciente_delete'),  
    path('especialidades/', especialidades, name='especialidades'),



]
