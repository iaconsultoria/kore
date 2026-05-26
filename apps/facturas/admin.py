from django.contrib import admin
from .models import Factura

# Register your models here.

@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = (
        "numero_factura",
        "fecha_emision",
        "nif_emisor",
        "nombre_emisor",
        "total",
    )

    search_fields = (
        "numero_factura",
        "nif_emisor",
        "nombre_emisor",
    )

    list_filter = (
        "fecha_emision",
    )
