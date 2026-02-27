from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from posts.models import Post, Feedback
from .forms import FeedbackForm  # Você precisará criar este forms.py

# HOME (com posts ordenados)
def home(request):
    searchBox = request.GET.get('campoBuscaHome', '')

    # Melhorando a busca para título E conteúdo
    if searchBox:
        posts = Post.objects.filter(
            Q(titulo__icontains=searchBox) | 
            Q(conteudo__icontains=searchBox)
        ).order_by('-criado_em')
    else:
        posts = Post.objects.all().order_by('-criado_em')

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
        "form": form,
        "termo_busca": searchBox
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

# OUTRAS VIEWS
def about_view(request):
    return HttpResponse("Sobre nós")

def contact_view(request):
    return HttpResponse("Contato")

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

    return render(request, 'documentos.html', {
        'posts': posts,
        'busca': termo_de_busca
    })