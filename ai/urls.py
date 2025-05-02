from django.urls import path
from . import views

urlpatterns = [
    path('generar-campaña/', views.generarar_campaña, name='generar_campaña'),
]
