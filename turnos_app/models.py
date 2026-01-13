import os
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Especialidad(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    activa = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Especialidad"
        verbose_name_plural = "Especialidades"


    def __str__(self):
        return self.nombre
    

class Profesional(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    matricula = models.CharField(max_length=50, unique=True)
    especialidad = models.ForeignKey(
        Especialidad,
        on_delete=models.PROTECT,
        related_name="profesionales"
    )
    email = models.EmailField(blank=True, null=True)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Profesional"
        verbose_name_plural = "Profesionales"

    def __str__(self):
        return f"{self.apellido}, {self.nombre} ({self.especialidad})"
    

class Paciente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dni = models.CharField(max_length=20, unique=True)
    fecha_nacimiento = models.DateField()
    telefono = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        nombre = self.user.first_name.strip()
        apellido = self.user.last_name.strip()

        if nombre or apellido:
            return f"{apellido}, {nombre}".strip(", ")
        return f"Paciente DNI {self.dni}"




    
class Turno(models.Model):

    ESTADO_CHOICES = [
        ('reservado', 'Reservado'),
        ('cancelado', 'Cancelado'),
        ('atendido', 'Atendido'),
        ('ausente', 'Ausente'),
    ]

    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        related_name="turnos"
    )
    profesional = models.ForeignKey(
        Profesional,
        on_delete=models.PROTECT,
        related_name="turnos"
    )
    fecha = models.DateField()
    hora = models.TimeField()
    estado = models.CharField(
        max_length=10,
        choices=ESTADO_CHOICES,
        default='reservado'
    )
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('profesional', 'fecha', 'hora')
        ordering = ['fecha', 'hora']

    def __str__(self):
        return f"{self.fecha} {self.hora} - {self.paciente} con {self.profesional}"
    


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(
        upload_to='avatars/',
        default='avatars/default.png'
    )

    def save(self, *args, **kwargs):
        if self.pk:
            old = Profile.objects.get(pk=self.pk)

            
            default_path = 'avatars/default.png'

            if (
                old.avatar
                and old.avatar.name != default_path
                and old.avatar != self.avatar
            ):
                if os.path.isfile(old.avatar.path):
                    os.remove(old.avatar.path)

        super().save(*args, **kwargs)

