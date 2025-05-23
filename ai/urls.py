from django.urls import path
from .views import api_match

urlpatterns = [
    path('match/', api_match, name='api_match'),
]
