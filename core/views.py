from django.shortcuts import render
from django.http import HttpResponse
from posts.models import Post  # 👈 importa o model

# HOME (agora dinâmica com banco)
def home(request):
    posts = Post.objects.all()  # pega todos os posts do banco
    return render(request, "home.html", {"posts": posts})


# VIEWS SIMPLES (placeholders por enquanto)
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