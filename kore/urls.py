from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('facturas/', include('apps.facturas.urls')),
    path("calendario/", include("apps.calendario.urls")),
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
