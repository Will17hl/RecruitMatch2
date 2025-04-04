from django.urls import path
from . import views

urlpatterns = [
    path('', views.applicant_form, name='applyJob'),
]