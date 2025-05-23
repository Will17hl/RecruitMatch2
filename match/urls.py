from django.urls import path
from .views import api_match

app_name = 'match'

urlpatterns = [
    path('', api_match, name='api_match'),
    path('api/', api_match, name='api_match_api'),  # opcional
]

