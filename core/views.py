from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from posts.models import Post, Feedback
from posts.forms import FeedbackForm  # Você precisará criar este forms.py


# ===============================
# 🏠 HOME (com posts ordenados)
# ===============================
def home(request):
    searchBox = request.GET.get('campoBuscaHome', '')

<<<<<<< HEAD
    posts = Post.objects.filter(
        titulo__contains=searchBox
    ).order_by('-criado_em')
=======
    # Melhorando a busca para título E conteúdo
    if searchBox:
        posts = Post.objects.filter(
            Q(titulo__icontains=searchBox) | 
            Q(conteudo__icontains=searchBox)
        ).order_by('-criado_em')
    else:
        posts = Post.objects.all().order_by('-criado_em')
>>>>>>> 6460ebb21dfae68d1728bf735d758cc16868991b

    # Processar comentário rápido da home
    if request.method == 'POST' and 'post_id' in request.POST:
        post_id = request.POST.get('post_id')
        post_instancia = get_object_or_404(Post, id=post_id)
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.post = post_instancia
            feedback.usuario = request.user
            feedback.save()
            return redirect('home')

    form = FeedbackForm()
    
    return render(request, "home.html", {
        "posts": posts,
<<<<<<< HEAD
        "busca": searchBox
=======
        "form": form,
        "termo_busca": searchBox
>>>>>>> 6460ebb21dfae68d1728bf735d758cc16868991b
    })

# NOVA VIEW: Detalhe do Post com comentários
def detalhe_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    feedbacks = post.feedbacks.all().order_by('-data_envio')
    
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.post = post
            feedback.usuario = request.user
            feedback.save()
            return redirect('detalhe_post', post_id=post.id)
    else:
        form = FeedbackForm()

    total_comentarios = feedbacks.count()
    
    return render(request, 'detalhe_post.html', {
        'post': post,
        'feedbacks': feedbacks,
        'form': form,
        'total_comentarios': total_comentarios,
    })

# NOVA VIEW: Central de Comentários
def central_comentarios(request):
    # Pega todos os feedbacks com informações dos posts e usuários
    todos_feedbacks = Feedback.objects.select_related('post', 'usuario').all().order_by('-data_envio')
    
    # Estatísticas
    total_comentarios = todos_feedbacks.count()
    total_posts_comentados = Feedback.objects.values('post').distinct().count()
    
    # Top 5 usuários mais ativos
    usuarios_mais_ativos = Feedback.objects.values('usuario__username').annotate(
        total=Count('id')
    ).order_by('-total')[:5]
    
    # Posts mais comentados
    posts_mais_comentados = Post.objects.annotate(
        total_comentarios=Count('feedbacks')
    ).filter(total_comentarios__gt=0).order_by('-total_comentarios')[:5]
    
    # Filtro por post ou usuário
    filtro = request.GET.get('filtro')
    if filtro:
        todos_feedbacks = todos_feedbacks.filter(
            Q(post__titulo__icontains=filtro) |
            Q(usuario__username__icontains=filtro) |
            Q(comentario__icontains=filtro)
        )
    
    context = {
        'feedbacks': todos_feedbacks,
        'total_comentarios': total_comentarios,
        'total_posts_comentados': total_posts_comentados,
        'usuarios_mais_ativos': usuarios_mais_ativos,
        'posts_mais_comentados': posts_mais_comentados,
        'filtro': filtro,
    }
    return render(request, 'central_comentarios.html', context)

# ===============================
# 🔐 LOGIN / LOGOUT (placeholder)
# ===============================
def login_view(request):
    return HttpResponse("Página de Login")

def logout_view(request):
    return HttpResponse("Logout realizado")

def register_view(request):
    return HttpResponse("Página de Registro")

<<<<<<< HEAD

# ===============================
# 👤 PERFIL + PUBLICAÇÃO
# ===============================
@login_required
def profile_view(request):

=======
# PERFIL + PUBLICAÇÃO
def profile_view(request):
    # 🔥 Quando clicar no botão "Publicar"
>>>>>>> 6460ebb21dfae68d1728bf735d758cc16868991b
    if request.method == "POST":
        titulo = request.POST.get("titulo")
        conteudo = request.POST.get("conteudo")

        if titulo and conteudo:
            Post.objects.create(
                titulo=titulo,
                conteudo=conteudo,
                autor=request.user
            )
<<<<<<< HEAD

            return redirect("/")
=======
            return redirect("/")  # volta pra home
>>>>>>> 6460ebb21dfae68d1728bf735d758cc16868991b

    # Adicionar comentários do usuário no perfil
    if request.user.is_authenticated:
        meus_comentarios = Feedback.objects.filter(
            usuario=request.user
        ).select_related('post').order_by('-data_envio')
        
        total_comentarios = meus_comentarios.count()
        posts_comentados = meus_comentarios.values('post').distinct().count()
    else:
        meus_comentarios = []
        total_comentarios = 0
        posts_comentados = 0

    return render(request, "profile.html", {
        'meus_comentarios': meus_comentarios,
        'total_comentarios': total_comentarios,
        'posts_comentados': posts_comentados,
    })

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

<<<<<<< HEAD

# ===============================
# 📚 DOCUMENTOS
# ===============================
def documents(request):
    termo_de_busca = request.GET.get('busca', '')

    posts = Post.objects.filter(
        titulo__contains=termo_de_busca
    ).order_by('-criado_em')
=======
# DOCUMENTOS (mostrar apenas posts com arquivo)
def documents(request):
    termo_de_busca = request.GET.get('busca', '')

    if termo_de_busca:
        posts = Post.objects.filter(
            Q(titulo__icontains=termo_de_busca) | 
            Q(conteudo__icontains=termo_de_busca),
            arquivo__isnull=False
        ).exclude(arquivo='').order_by('-criado_em')
    else:
        posts = Post.objects.exclude(arquivo='').order_by('-criado_em')
>>>>>>> 6460ebb21dfae68d1728bf735d758cc16868991b

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