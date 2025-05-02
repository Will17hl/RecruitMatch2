from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required


# Vista para registrar una nueva cuenta
def signupaccount(request):
    if request.method == 'GET':
        return render(request, 'signupaccount.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'],
                    password=request.POST['password1']
                )
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'signupaccount.html', {
                    'form': UserCreationForm(),
                    'error': 'El nombre de usuario ya está en uso. Intenta con otro.'
                })
        else:
            return render(request, 'signupaccount.html', {
                'form': UserCreationForm(),
                'error': 'Las contraseñas no coinciden.'
            })


# Vista para iniciar sesión
def loginaccount(request):
    if request.method == 'GET':
        return render(request, 'loginaccount.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request,
                            username=request.POST['username'],
                            password=request.POST['password'])

        if user is None:
            return render(request, 'loginaccount.html', {
                'form': AuthenticationForm(),
                'error': 'El usuario y la contraseña no coinciden.'
            })
        else:
            login(request, user)
            return redirect('home')


# Vista para cerrar sesión
@login_required
def logoutaccount(request):
    logout(request)
    return redirect('home')


# Vista del perfil, mostrando solo la información básica del usuario
@login_required
def profile_view(request):
    # Solo se muestra la información básica del usuario sin preferencias.
    context = {
        'username': request.user.username,
        'email': request.user.email,
        'date_joined': request.user.date_joined.strftime('%d/%m/%Y'),
    }

    return render(request, 'account.html', context)
