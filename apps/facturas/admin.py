from django.contrib import admin
from .models import Factura, LineaFactura, Proveedor, CategoriaGasto


class LineaFacturaInline(admin.TabularInline):
    model = LineaFactura
    extra = 1


@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ("numero_factura", "fecha_emision", "proveedor", "total")
    search_fields = ("numero_factura",)
    list_filter = ("fecha_emision",)
    inlines = [LineaFacturaInline]


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ("nombre", "nif", "pais")


@admin.register(CategoriaGasto)
class CategoriaGastoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "deducible_iva", "cuenta_contable")
