from django.urls import path
from . import views

urlpatterns = [
    path('revisar/<int:pk>/', views.revisar_extraccion, name='revisar_extraccion'),
    path('revisar/<int:pk>/comprobar-duplicado/', views.comprobar_duplicado, name='comprobar_duplicado'),
]
