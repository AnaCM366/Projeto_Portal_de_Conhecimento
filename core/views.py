from django.shortcuts import render, redirect
from django.http import HttpResponse
from posts.models import Post


# HOME (com posts ordenados)
def home(request):
    posts = Post.objects.all().order_by('-criado_em')

    return render(request, "home.html", {
        "posts": posts
    })


# LOGIN / LOGOUT (placeholder por enquanto)
def login_view(request):
    return HttpResponse("Página de Login")


def logout_view(request):
    return HttpResponse("Logout realizado")


def register_view(request):
    return HttpResponse("Página de Registro")


# PERFIL + PUBLICAÇÃO
def profile_view(request):

    # 🔥 Quando clicar no botão "Publicar"
    if request.method == "POST":
        titulo = request.POST.get("titulo")
        conteudo = request.POST.get("conteudo")

        # validação simples
        if titulo and conteudo:
            Post.objects.create(
                titulo=titulo,
                conteudo=conteudo,
                autor=request.user
            )

            return redirect("/")  # volta pra home

    return render(request, "profile.html")


# OUTRAS VIEWS
def about_view(request):
    return HttpResponse("Sobre nós")


def contact_view(request):
    return HttpResponse("Contato")


def documents(request):
    return HttpResponse("Documentos")