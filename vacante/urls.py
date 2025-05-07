from django.urls import path
from . import views

urlpatterns = [
    path('', views.vista_vacante, name='vacantes'),
    path('buscar_vacante/', views.buscar_vacante, name='buscar_vacante'),
]