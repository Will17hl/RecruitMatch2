from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import profile_view

urlpatterns = [
    path('signupaccount/', views.signupaccount, name='signupaccount'),
    path('loginaccount/', views.loginaccount, name='loginaccount'),
    path('logout/', views.logoutaccount, name='logoutaccount'),
    path('perfil/', profile_view, name='profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)