from django.urls import path
from . import views

urlpatterns = [
    path('', views.vista_influencer, name='influencers'),  # Ruta para ver los influencers
    path('buscar_influencers/', views.buscar_influencer, name='buscar_influencer'),  # Ruta para la búsqueda de influencers
]
