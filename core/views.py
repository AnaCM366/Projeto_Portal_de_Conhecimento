from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from posts.models import Post


# ===============================
# 🏠 HOME (com posts ordenados)
# ===============================
def home(request):
    searchBox = request.GET.get('campoBuscaHome', '')

    posts = Post.objects.filter(
        titulo__contains=searchBox
    ).order_by('-criado_em')

    return render(request, "home.html", {
        "posts": posts,
        "busca": searchBox
    })


# ===============================
# 🔐 LOGIN / LOGOUT (placeholder)
# ===============================
def login_view(request):
    return HttpResponse("Página de Login")


def logout_view(request):
    return HttpResponse("Logout realizado")


def register_view(request):
    return HttpResponse("Página de Registro")


# ===============================
# 👤 PERFIL + PUBLICAÇÃO
# ===============================
@login_required
def profile_view(request):

    if request.method == "POST":
        titulo = request.POST.get("titulo")
        conteudo = request.POST.get("conteudo")

        if titulo and conteudo:
            Post.objects.create(
                titulo=titulo,
                conteudo=conteudo,
                autor=request.user
            )

            return redirect("/")

    return render(request, "profile.html")


# ===============================
# 📄 DETALHE DO POST
# ===============================
def detalhe_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    return render(request, "detalhe_post.html", {
        "post": post
    })


# ===============================
# 💬 CENTRAL DE COMENTÁRIOS (Mock)
# ===============================
def central_comentarios(request):
    return HttpResponse("Central de comentários - Em desenvolvimento")


# ===============================
# ℹ OUTRAS VIEWS
# ===============================
def about_view(request):
    return HttpResponse("Sobre nós")


def contact_view(request):
    return HttpResponse("Contato")


# ===============================
# 📚 DOCUMENTOS
# ===============================
def documents(request):
    termo_de_busca = request.GET.get('busca', '')

    posts = Post.objects.filter(
        titulo__contains=termo_de_busca
    ).order_by('-criado_em')

    return render(request, 'documentos.html', {
        'posts': posts,
        'busca': termo_de_busca
    })


# ===============================
# 💰 FATURAMENTO (Mock Demonstrativo)
# ===============================
@login_required
def faturamento(request):

    dados = {
        "total_atual": 36200.00,
        "total_anterior": 25700.00,
        "crescimento": 40.67,
        "por_categoria": [
            {"nome": "Planos Premium", "valor": 21256.98},
            {"nome": "Assinaturas Básicas", "valor": 15110.22},
        ],
        "percentuais": [
            {"mes": "Jan", "valor": 50},
            {"mes": "Fev", "valor": 43},
            {"mes": "Mar", "valor": 27},
            {"mes": "Abr", "valor": 48},
            {"mes": "Mai", "valor": 62},
            {"mes": "Jun", "valor": 22},
        ]
    }

    return render(request, "faturamento.html", {"dados": dados})