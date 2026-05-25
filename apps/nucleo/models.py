from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError
class Rol(models.TextChoices):
    ADMIN = "admin", "Administrador"
    OPERADOR = "operador", "Operador"
    SOLO_LECTURA="solo_lectura", "Solo lectura"

class Perfil(models.Model):
    usuario= models.OneToOneField(
        User, on_delete=models.CASCADE,
        related_name="perfil"
    ) 
    rol= models.CharField(
        max_length=20,
        choices=Rol.choices,
        default=Rol.OPERADOR
    )
    telefono=models.CharField(
        max_length=20,
        blank=True,
        default=""
    )
    cargo=models.CharField(
        max_length=100,
        blank=True,
        default=""
    )
    actualizado_en=models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfiles"

    def __str__(self):
        return f"Perfil de {self.usuario.username} ({self.get_rol_display()})"    
   
    @property
    def es_admin(self) -> bool:
        return self.rol==Rol.ADMIN
    
    @property
    def es_operador(self) -> bool:
        return self.rol ==Rol.OPERADOR
    
    @property
    def es_solo_lectura(self) -> bool:
        return self.rol==Rol.SOLO_LECTURA
