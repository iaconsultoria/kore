from django.contrib import admin
from .models import Perfil
from .models import Negocio
@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'rol', 'cargo')
    search_fields = ('usuario__username', 'usuario__email', 'cargo')
    list_filter = ('rol',)

@admin.register(Negocio)
class NegocioAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "identificador_fiscal",
        "pais",
        "actualizado_en",
    )
