from django.contrib import admin
from django.urls import path, include
from .views import *
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', inicio, name='inicio'),  # Ruta raíz redirige al admin
   
    path("turnos/", TurnoListView.as_view(), name="turno_list"),
    path("turnos/nuevo/", TurnoCreateView.as_view(), name="turno_create"),
    path("turnos/editar/<int:pk>/", TurnoUpdateView.as_view(), name="turno_update"),
    path("turnos/eliminar/<int:pk>/", TurnoDeleteView.as_view(), name="turno_delete"),

    path("profesionales/", ProfesionalListView.as_view(), name="profesional_list"),
  
    path("pacientes/", PacienteListView.as_view(), name="paciente_list"),
    path("pacientes/nuevo/", PacienteCreateView.as_view(), name="paciente_create"),
    path("pacientes/<int:pk>/editar/", PacienteUpdateView.as_view(), name="paciente_update"),
    path("pacientes/<int:pk>/eliminar/", PacienteDeleteView.as_view(), name="paciente_delete"),

    path('especialidades/', EspecialidadListView.as_view(), name='especialidad_list'),

    # Buscar turnos
    path('buscar_turnos/', buscar_turnos, name='buscar_turnos'),
    path('encontrar_turnos/', encontrar_turnos, name='encontrar_turnos'),

    # login / logout / registration
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='inicio'), name='logout'),
    path('register/', register, name='register'),
    path('perfil/', perfil, name='perfil'),
    path('avatar/', avatar, name='avatar'),

]
