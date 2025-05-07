from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Vacante  # Asegúrate de que el modelo Vacante esté importado
from django.db.models import Q

# Vista para mostrar las vacantes con filtros y paginación
def vista_vacante(request):
    vacantes = Vacante.objects.all()  # Obtener todas las vacantes inicialmente

    # Filtro por nombre de la vacante
    filtro_nombre = request.GET.get('nombre_vacante', '')
    if filtro_nombre:
        vacantes = vacantes.filter(nombre_vacante__icontains=filtro_nombre)

    # Filtro por id de la vacante
    filtro_id = request.GET.get('id_vacante', '')
    if filtro_id:
        try:
            vacantes = vacantes.filter(id_vacante=int(filtro_id))
        except ValueError:
            pass

    # Filtro por ciudad de la vacante
    filtro_ciudad = request.GET.get('ciudad_vacante', '')
    if filtro_ciudad:
        vacantes = vacantes.filter(ciudad_vacante__icontains=filtro_ciudad)

    # Filtro por área de la vacante
    filtro_area = request.GET.get('area_vacante', '')
    if filtro_area:
        vacantes = vacantes.filter(area_vacante__icontains=filtro_area)

    # Filtro por salario de la vacante
    filtro_salario = request.GET.get('salario_vacante', '')
    if filtro_salario:
        try:
            vacantes = vacantes.filter(salario_vacante__gte=int(filtro_salario))
        except ValueError:
            pass

    # Filtro por empresa de la vacante
    filtro_empresa = request.GET.get('empresa_vacante', '')
    if filtro_empresa:
        vacantes = vacantes.filter(empresa_vacante__icontains=filtro_empresa)

    # Paginación
    paginador = Paginator(vacantes, 12)  # Mostrar 12 vacantes por página
    numero_pagina = request.GET.get('page')
    page_obj = paginador.get_page(numero_pagina)

    return render(request, 'vacante.html', {'page_obj': page_obj})

# Vista para manejar la búsqueda (reutilizada en la vista principal)
def buscar_vacante(request):
    return vista_vacante(request)
