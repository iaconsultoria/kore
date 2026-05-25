from django.contrib import admin
from .models import Negocio


@admin.register(Negocio)
class NegocioAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "identificador_fiscal",
        "pais",
        "actualizado_en",
    )
