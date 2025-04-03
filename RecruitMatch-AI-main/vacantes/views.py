from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm
from django.contrib import messages
from .models import Vacante

def home(request):
    vacantes = Vacante.objects.all().order_by('-date')[:6]  # Obtener las 6 últimas vacantes
    return render(request, 'home.html', {'vacantes': vacantes})

def vacantes_list(request):
    vacantes = Vacante.objects.all().order_by('-date')
    return render(request, 'vacantes/vacantes_list.html', {'vacantes': vacantes})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '¡Registro exitoso! Bienvenido a RecruitMatch.')
            return redirect('home')
        else:
            messages.error(request, 'Por favor, corrige los errores en el formulario.')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'registration/profile.html')