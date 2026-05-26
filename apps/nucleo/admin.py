from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse
from .models import Perfil, Negocio
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

    def has_add_permission(self, request):
        # Oculta el botón "Añadir" si ya existe una instancia.
        return not Negocio.objects.exists()

    def add_view(self, request, form_url='', extra_context=None):
        # Segunda línea de defensa: si alguien llega a la URL
        # directamente (/admin/nucleo/negocio/add/) lo redirige
        # a editar la instancia existente en lugar de dar un error.
        if Negocio.objects.exists():
            obj = Negocio.objects.get()
            return redirect(
                reverse('admin:nucleo_negocio_change', args=[obj.pk])
            )
        return super().add_view(request, form_url, extra_context)
