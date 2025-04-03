from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Vacante

def home(request):
    vacantes = Vacante.objects.all()

    # Get search parameters
    search_query = request.GET.get('searchvacante', '')
    company_filter = request.GET.get('company', '')
    location_filter = request.GET.get('location', '')
    area_filter = request.GET.get('area', '')

    # Apply filters
    if search_query:
        vacantes = vacantes.filter(title__icontains=search_query)
    if company_filter:
        vacantes = vacantes.filter(company__icontains=company_filter)
    if location_filter:
        vacantes = vacantes.filter(location__icontains=location_filter)
    if area_filter:
        vacantes = vacantes.filter(area__icontains=area_filter)

    # Paginate results
    paginator = Paginator(vacantes, 12)  # Show 10 jobs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'home.html', {
        'page_obj': page_obj,
        'searchvacante': search_query,
        'company': company_filter,
        'location': location_filter,
        'area': area_filter,
    })
def signup(request):
    return render(request, 'signup.html')