from django.contrib import admin
from .models import ConfiguracionGlobal

# Register your models here.
@admin.register(ConfiguracionGlobal)
class ConfiguracionGlobalAdmin(admin.ModelAdmin):
    # Esto hará que en el listado del admin se vean todos estos campos como columnas
    list_display = ('nombre_instancia', 'version', 'fecha_creacion')