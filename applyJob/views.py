from django.shortcuts import render, redirect
from .models import Applicant

def applicant_form(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        cc = request.POST.get('cc')
        estudios = request.POST.get('estudios')
        tipo = request.POST.get('tipo')
        correo = request.POST.get('correo')

        Applicant.objects.create(
            nombre=nombre,
            cc=cc,
            estudios=estudios,
            tipo=tipo,
            correo=correo
        )
        return redirect('success')  # Redirige a una página de éxito

    return render(request, 'applicant_form.html')