from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q, Count

from posts.models import Post, Feedback
from posts.forms import FeedbackForm


# =========================
# HOME (COM BUSCA + COMENTÁRIO RÁPIDO)
# =========================

@login_required
def home(request):
    searchBox = request.GET.get('campoBuscaHome', '')

    if searchBox:
        posts = Post.objects.filter(
            Q(titulo__icontains=searchBox) |
            Q(conteudo__icontains=searchBox)
        ).order_by('-criado_em')
    else:
        posts = Post.objects.all().order_by('-criado_em')

    # Comentário rápido na home
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
        "form": form,
        "termo_busca": searchBox
    })


# =========================
# DETALHE DO POST
# =========================

@login_required
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


# =========================
# CENTRAL DE COMENTÁRIOS
# =========================

@login_required
def central_comentarios(request):

    todos_feedbacks = Feedback.objects.select_related(
        'post', 'usuario'
    ).all().order_by('-data_envio')

    total_comentarios = todos_feedbacks.count()
    total_posts_comentados = Feedback.objects.values('post').distinct().count()

    usuarios_mais_ativos = Feedback.objects.values(
        'usuario__username'
    ).annotate(
        total=Count('id')
    ).order_by('-total')[:5]

    posts_mais_comentados = Post.objects.annotate(
        total_comentarios=Count('feedbacks')
    ).filter(total_comentarios__gt=0).order_by('-total_comentarios')[:5]

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


# =========================
# LOGIN (COM REDIRECIONAMENTO INTELIGENTE)
# =========================

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # 🔥 Redireciona para ?next= se existir
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)

            return redirect("home")
        else:
            messages.error(request, "Usuário ou senha inválidos")

    return render(request, "login.html")


# =========================
# LOGOUT
# =========================

@login_required
def logout_view(request):
    logout(request)
    return redirect("login")


# =========================
# REGISTER
# =========================

def register_view(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Usuário já existe")
        else:
            User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            messages.success(request, "Conta criada com sucesso!")
            return redirect("login")

    return render(request, "register.html")


# =========================
# PERFIL + PUBLICAÇÃO
# =========================

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
            return redirect("home")

    meus_comentarios = Feedback.objects.filter(
        usuario=request.user
    ).select_related('post').order_by('-data_envio')

    total_comentarios = meus_comentarios.count()
    posts_comentados = meus_comentarios.values('post').distinct().count()

    return render(request, "profile.html", {
        'meus_comentarios': meus_comentarios,
        'total_comentarios': total_comentarios,
        'posts_comentados': posts_comentados,
    })


# =========================
# PÁGINAS INSTITUCIONAIS
# =========================

def about_view(request):
    return render(request, "about.html")


def contact_view(request):
    return render(request, "contact.html")


# =========================
# DOCUMENTOS
# =========================

@login_required
def documents(request):

    termo_de_busca = request.GET.get('busca', '')

    if termo_de_busca:
        posts = Post.objects.filter(
            Q(titulo__icontains=termo_de_busca) |
            Q(conteudo__icontains=termo_de_busca),
            arquivo__isnull=False
        ).exclude(arquivo='').order_by('-criado_em')
    else:
        posts = Post.objects.exclude(
            arquivo=''
        ).order_by('-criado_em')

    return render(request, 'documentos.html', {
        'posts': posts,
        'busca': termo_de_busca
    })


# =========================
# FATURAMENTO
# =========================

@login_required
def faturamento(request):
    return render(request, 'faturamento.html')