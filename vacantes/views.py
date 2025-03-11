from django.shortcuts import render
from .models import Vacante

def home(request):
    searchVacante = request.GET.get('searchMovie')
    if searchVacante:
        vacantes = Vacante.objects.filter(title__icontains=searchVacante)
    else:    
        vacantes = Vacante.objects.all()
    return render(request, 'home.html', {'searchVacante':searchVacante, 'vacantes': vacantes})  

def signup(request):
    return render(request, 'signup.html')