from django.contrib import admin
from .models import Tenant


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ("nombre", "slug", "activo", "creado_en")
