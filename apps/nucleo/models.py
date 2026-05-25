from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError


class Negocio(models.Model):
    nombre = models.CharField(max_length=200)
    identificador_fiscal = models.CharField(max_length=50)
    pais = models.CharField(max_length=2, default="ES")
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre


class Rol(models.TextChoices):
    ADMIN = "admin", "Administrador"
    OPERADOR = "operador", "Operador"
    SOLO_LECTURA="solo_lectura", "Solo lectura"


class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name="perfil")
    rol = models.CharField(max_length=20, choices=Rol.choices, default=Rol.OPERADOR)
    telefono = models.CharField(max_length=20, blank=True, default="")
    cargo = models.CharField(max_length=100, blank=True, default="")
    actualizado_en = models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfiles"

    
    def __str__(self):
        return f"Perfil de {self.usuario.username} ({self.get_rol_display()})"    
   

