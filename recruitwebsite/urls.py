"""
URL configuration for recruitwebsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from accounts import views as accountViews
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signupaccount/', accountViews.signupaccount),
    path('accounts/', include('accounts.urls')),
    path('loginaccount/', accountViews.loginaccount),
    path('perfil/', accountViews.profile_view, name='profile'),
    path('ai/', include('ai.urls')),
    path('influencer/', include('influencer.urls')),
    path('vacante/', include('vacante.urls')),
    path('match/', include('match.urls', namespace='match')),  # Aquí incluyes las URLs de match con namespace
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
