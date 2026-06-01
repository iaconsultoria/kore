from django.contrib import admin
from .models import Categoria, Cita, Recordatorio

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ["nombre", "color", "prioridad", "politica_reprog"]

@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ["titulo", "inicio", "fin", "categoria", "prioridad", "repetir"]

@admin.register(Recordatorio)
class RecordatorioAdmin(admin.ModelAdmin):
    list_display = ["cita", "fecha_aviso", "tipo"]
