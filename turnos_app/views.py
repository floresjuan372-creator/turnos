from urllib import request
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.contrib.auth import authenticate, login



# Create your views here.

def inicio(request):
    return render(request, 'turnos_app/index.html')



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

class PacienteListView(LoginRequiredMixin, ListView):
    model = Paciente
    template_name = "turnos_app/paciente_list.html"
    context_object_name = "pacientes"

    def get_queryset(self):
        return Paciente.objects.filter(user=self.request.user)

class PacienteCreateView(LoginRequiredMixin, CreateView):
    model = Paciente
    form_class = PacienteForm
    template_name = "turnos_app/paciente_form.html"
    success_url = reverse_lazy("paciente_list")

    def dispatch(self, request, *args, **kwargs):
        
        if not request.user.is_staff:
            return redirect("inicio")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
       
        return super().form_valid(form)


class PacienteUpdateView(LoginRequiredMixin, UpdateView):
    model = Paciente
    form_class = PacienteForm
    template_name = "turnos_app/paciente_form.html"
    success_url = reverse_lazy("paciente_list")

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_staff:
            return qs
        return qs.filter(user=self.request.user)





class PacienteDeleteView(LoginRequiredMixin, DeleteView):
    model = Paciente
    template_name = "turnos_app/paciente_confirm_delete.html"
    success_url = reverse_lazy("paciente_list")

class ProfesionalListView(LoginRequiredMixin, ListView):
    model = Profesional
    template_name = "turnos_app/profesional_list.html"
    context_object_name = "profesionales"

class TurnoListView(LoginRequiredMixin, ListView):
    model = Turno
    template_name = "turnos_app/turno_list.html"
    context_object_name = "turnos"

    def get_queryset(self):
        
        if self.request.user.is_staff:
            return Turno.objects.all()

       
        return Turno.objects.filter(paciente__user=self.request.user)


class TurnoCreateView(LoginRequiredMixin, CreateView):
    model = Turno
    form_class = TurnoForm
    template_name = "turnos_app/turno_form.html"
    success_url = reverse_lazy("turno_list")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        
        if not self.request.user.is_staff:
            form.fields['paciente'].queryset = Paciente.objects.filter(
                user=self.request.user
            )

        return form


class TurnoUpdateView(LoginRequiredMixin, UpdateView):
    model = Turno
    form_class = TurnoForm
    template_name = "turnos_app/turno_form.html"
    success_url = reverse_lazy("turno_list")


class TurnoDeleteView(LoginRequiredMixin, DeleteView):
    model = Turno
    template_name = "turnos_app/turno_confirm_delete.html"
    success_url = reverse_lazy("turno_list")


class EspecialidadListView(LoginRequiredMixin, ListView):
    model = Especialidad
    template_name = 'turnos_app/especialidad_list.html'
    context_object_name = 'especialidades'


# Página del buscador
@login_required
def buscar_turnos(request):
    return render(request, 'turnos_app/buscar_turnos.html')


# Lógica de búsqueda
@login_required
def encontrar_turnos(request):
    patron = request.GET.get("buscar", "").strip()

    
    if request.user.is_staff:
      
        queryset = Turno.objects.all()
    else:
    
        queryset = Turno.objects.filter(paciente__user=request.user)

    
    if patron:
        turnos = queryset.filter(
            Q(paciente__user__first_name__icontains=patron) |
            Q(paciente__user__last_name__icontains=patron) |
            Q(profesional__nombre__icontains=patron) |
            Q(profesional__apellido__icontains=patron)
        )
    else:
        turnos = queryset

    return render(
        request,
        'turnos_app/turno_list.html',
        {'turnos': turnos}
    )

# login / logaut / registration

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('inicio')
    



def register(request):
    if request.method == "POST":
        form = registroform(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data["email"]
            user.first_name = form.cleaned_data["first_name"]
            user.last_name = form.cleaned_data["last_name"]
            user.save()

            
            Paciente.objects.create(
                user=user,
                dni=form.cleaned_data["dni"],
                fecha_nacimiento=form.cleaned_data["fecha_nacimiento"],
                telefono=form.cleaned_data.get("telefono", "")
            )

            login(request, user)
            return redirect("inicio")
    else:
        form = registroform()

    return render(request, "registration/register.html", {"form": form})



@login_required
def perfil(request):
    user = request.user

    
    profile, _ = Profile.objects.get_or_create(user=user)
    paciente, _ = Paciente.objects.get_or_create(
        user=user,
        defaults={
            'dni': f"TMP-{user.id}",
            'fecha_nacimiento': '2000-01-01'
        }
    )

    if request.method == 'POST':
        user_form = profileform(request.POST, instance=user)
        paciente_form = PacientePerfilForm(request.POST, instance=paciente)

        if user_form.is_valid() and paciente_form.is_valid():
            user_form.save()
            paciente_form.save()
            return redirect('perfil')
    else:
        user_form = profileform(instance=user)
        paciente_form = PacientePerfilForm(instance=paciente)

    return render(
        request,
        'registration/perfil.html',
        {
            'user_form': user_form,
            'paciente_form': paciente_form,
        }
    )



@login_required
def avatar(request):
    perfil, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = avatarform(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            return redirect('perfil')
    else:
        form = avatarform(instance=perfil)

    return render(request, 'registration/avatar.html', {'form': form})