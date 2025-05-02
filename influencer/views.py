from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Influencer
from django.db.models import Q

# Vista para mostrar los influencers con filtros y paginación
def vista_influencer(request):
    influencers = Influencer.objects.all()  # Obtener todos los influencers inicialmente

    # Filtro por ciudad
    filtro_ciudad = request.GET.get('ciudad_influencer', '')
    if filtro_ciudad:
        influencers = influencers.filter(ciudad_influencer__icontains=filtro_ciudad)

    # Filtro por nombre de influencer
    filtro_nombre = request.GET.get('nombre_influencer', '')
    if filtro_nombre:
        influencers = influencers.filter(nombre_influencer__icontains=filtro_nombre)

    # Filtro por área del influencer
    filtro_area = request.GET.get('area_influencer', '')
    if filtro_area:
        influencers = influencers.filter(area_influencer__icontains=filtro_area)

    # Filtro por cantidad de seguidores
    filtro_seguidores = request.GET.get('seguidores', '')
    if filtro_seguidores:
        try:
            seguidores = int(filtro_seguidores)
            influencers = influencers.filter(seguidores__gte=seguidores)
        except ValueError:
            pass

    # Filtro por precio de campaña
    filtro_precio = request.GET.get('precio_campaña', '')
    if filtro_precio:
        try:
            precio = float(filtro_precio)
            influencers = influencers.filter(precio_campaña__lte=precio)
        except ValueError:
            pass

    # Paginación
    paginador = Paginator(influencers, 18)  # Mostrar 18 influencers por página
    numero_pagina = request.GET.get('page')
    page_obj = paginador.get_page(numero_pagina)

    return render(request, 'influencers.html', {'page_obj': page_obj})

# Vista para manejar la búsqueda (reutilizada en la vista principal)
def buscar_influencer(request):
    return vista_influencer(request)
