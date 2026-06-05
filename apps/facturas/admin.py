from django.contrib import admin
from .models import Factura, LineaFactura, Proveedor, CategoriaGasto, FragmentoNormativa, SugerenciaCategoria

class LineaFacturaInline(admin.TabularInline):
    model = LineaFactura
    extra = 1


@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ("numero_factura", "fecha_emision", "proveedor", "total")
    search_fields = ("numero_factura",)
    list_filter = ("fecha_emision", "proveedor", "categoria")
    inlines = [LineaFacturaInline]


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ("nombre", "nif", "pais")
    search_fields = ("nombre", "nif")


@admin.register(CategoriaGasto)
class CategoriaGastoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "deducible_iva", "cuenta_contable")


@admin.register(FragmentoNormativa)
class FragmentoNormativaAdmin(admin.ModelAdmin):
    list_display = ('fuente', 'texto')


@admin.register(SugerenciaCategoria)
class SugerenciaCategoriaAdmin(admin.ModelAdmin):
    list_display = ('factura', 'texto_sugerencia', 'modelo_ia_usado', 'aceptada', 'fecha')
    list_filter = ('aceptada', 'fecha')
    search_fields = ('texto_sugerencia',)
    readonly_fields = ('fecha',)
