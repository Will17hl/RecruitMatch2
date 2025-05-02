from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    print("✅ Vista home ejecutada")
    return HttpResponse("CAMBIO HTML")

