# from django.shortcuts import render

# def home(request):
#   return render(request, "home.html")

from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, "home.html")

def login_view(request):
    return HttpResponse("Página de Login")

def logout_view(request):
    return HttpResponse("Logout realizado")

def register_view(request):
    return HttpResponse("Página de Registro")

def profile_view(request):
    return HttpResponse("Perfil do usuário")

def about_view(request):
    return HttpResponse("Sobre nós")

def contact_view(request):
    return HttpResponse("Contato")
  
def documents(request):
    return HttpResponse("Documentos")