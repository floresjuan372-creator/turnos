from urllib import request
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *


# Create your views here.

def inicio(request):
    return render(request, 'turnos_app/index.html')


def especialidades(request):
    especialidades = Especialidad.objects.filter(activa=True)
    return render(request, 'turnos_app/especialidades.html', {
        'especialidades': especialidades
    })


def profesionales(request):
    profesionales = Profesional.objects.filter(activo=True)
    return render(request, 'turnos_app/profesionales.html', {
        'profesionales': profesionales
    })


def pacientes(request):
    pacientes = Paciente.objects.all()
    return render(request, 'turnos_app/pacientes.html', {
        'pacientes': pacientes
    })



def turnos(request):
    turnos = Turno.objects.select_related(
        'paciente', 'profesional'
    )
    return render(request, 'turnos_app/turnos.html',{
        'turnos': turnos
    })

# Vista preparada para mostrar los turnos de un profesional específico, 
# actualmente sin uso en la interfaz pero lista para futuras funcionalidades.

def turnos_por_profesional(request, profesional_id):
    profesional = get_object_or_404(Profesional, id=profesional_id)
    turnos = Turno.objects.filter(profesional=profesional)

    return render(request, 'turnos_app/por_profesional.html', {
        'profesional': profesional,
        'turnos': turnos
    })

# Vista preparada para mostrar el historial de turnos de un paciente, 
# actualmente no utilizada pero disponible para futuras mejoras.

def turnos_por_paciente(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    turnos = Turno.objects.filter(paciente=paciente)

    return render(request, 'turnos_app/por_paciente.html', {
        'paciente': paciente,
        'turnos': turnos
    })


def crear_turno(request):
    if request.method == 'POST':
        form = TurnoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('turnos')
    else:
        form = TurnoForm()

    return render(request, 'turnos_app/crear_turno.html', {'form': form})



def crear_paciente(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_pacientes')
    else:
        form = PacienteForm()

    return render(request, 'turnos_app/crear_paciente.html', {'form': form})

def lista_pacientes(request):
    pacientes = Paciente.objects.all()
    return render(request, 'turnos_app/pacientes.html', {'pacientes': pacientes})

def turnoUpdate(request, id):
    turno = get_object_or_404(Turno, id=id)

    if request.method == 'POST':
        form = TurnoForm(request.POST, instance=turno)
        if form.is_valid():
            form.save()
            return redirect('turnos')
    else:
        form = TurnoForm(instance=turno)

    return render(
        request,
        'turnos_app/crear_turno.html',
        {'form': form}
    )

def turnoDelete(request, id):
    turno = get_object_or_404(Turno, id=id)

    if request.method == 'POST':
        turno.delete()
        return redirect('turnos')

    return render(
        request,
        'turnos_app/turno_delete.html',
        {'turno': turno}
    )

def pacienteUpdate(request, id):
    paciente = get_object_or_404(Paciente, id=id)

    if request.method == 'POST':
        form = PacienteForm(request.POST, instance=paciente)
        if form.is_valid():
            form.save()
            return redirect('pacientes')
    else:
        form = PacienteForm(instance=paciente)

    return render(
        request,
        'turnos_app/paciente_update.html',
        {'form': form, 'paciente': paciente}
    )

def pacienteDelete(request, id):
    paciente = get_object_or_404(Paciente, id=id)

    if request.method == 'POST':
        paciente.delete()
        return redirect('pacientes')

    return render(
        request,
        'turnos_app/paciente_delete.html',
        {'paciente': paciente}
    )

