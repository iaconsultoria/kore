from django.urls import path
from . import views
 
app_name = "calendario"
 
urlpatterns = [
    path("",                 views.cita_list,   name="cita_list"),
    path("nueva/",           views.cita_create, name="cita_create"),
    path("<int:pk>/editar/", views.cita_edit,   name="cita_edit"),
    path("<int:pk>/borrar/", views.cita_delete, name="cita_delete"),
    path("boton/", views.cita_boton, name="cita_boton"),
    path("desde-texto/", views.cita_desde_texto, name="cita_desde_texto"),
]