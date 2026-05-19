from django.db import models


# Modelo de la configuración
class ConfiguracionGlobal(models.Model):
    nombre_instancia = models.CharField(max_length=100)
    version = models.CharField(max_length=20)
    fecha_creacion= models.DateTimeField(auto_now_add=True)

# Sobrescribimos el método __str__
    def __str__(self):
        return self.nombre_instancia