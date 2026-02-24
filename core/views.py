from django.shortcuts import render
from django.http import HttpResponse
from posts.models import Post

def home(request):
    posts = Post.objects.all().order_by('-criado_em')  # 👈 corrigido

    return render(request, "home.html", {
        "posts": posts
    })


def login_view(request):
    return HttpResponse("Página de Login")

def logout_view(request):
    return HttpResponse("Logout realizado")

def register_view(request):
    return HttpResponse("Página de Registro")
# Perfil do usuario alterado para perfil, para evitar conflito com o app users
def profile_view(request):
    return render(request, "profile.html")

def about_view(request):
    return HttpResponse("Sobre nós")

def contact_view(request):
    return HttpResponse("Contato")

def documents(request):
    return HttpResponse("Documentos")