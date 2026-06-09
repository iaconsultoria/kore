from django.urls import path
from . import views
from .views import revisar_extraccion, comprobar_duplicado, avisos_vencimiento, lista_facturas, dashboard_fiscal, sugerir_categoria_view, aceptar_sugerencia_view, ignorar_sugerencia_view, mcp_endpoint

urlpatterns = [
    path('', views.lista_facturas, name='lista_facturas'),
    path('revisar/<int:pk>/', views.revisar_extraccion, name='revisar_extraccion'),
    path('revisar/<int:pk>/comprobar-duplicado/', views.comprobar_duplicado, name='comprobar_duplicado'),
    path('avisos-vencimiento/', views.avisos_vencimiento, name='avisos_vencimiento'),
    path('dashboard-fiscal/', views.dashboard_fiscal, name='dashboard_fiscal'),
    path('revisar/<int:pk>/sugerir-categoria/', views.sugerir_categoria_view, name='sugerir_categoria'),
    path('revisar/<int:pk>/aceptar-sugerencia/', views.aceptar_sugerencia_view, name='aceptar_sugerencia'),
    path('revisar/<int:pk>/ignorar-sugerencia/', views.ignorar_sugerencia_view, name='ignorar_sugerencia'),
    path('mcp/', mcp_endpoint, name='mcp_endpoint'),
]
