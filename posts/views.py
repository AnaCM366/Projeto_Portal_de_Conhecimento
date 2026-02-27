from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, Count
from .models import Post, Feedback
from .forms import FeedbackForm

# 🏠 Página Inicial
def home(request):
    buscarHome = request.GET.get('campoBuscaHome')
    
    if buscarHome and buscarHome.strip():
        postagens = Post.objects.filter(
            Q(titulo__icontains=buscarHome.strip()) |
            Q(conteudo__icontains=buscarHome.strip())
        ).order_by('-criado_em')
    else:
        postagens = Post.objects.all().order_by('-criado_em')

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
    
    context = {
        'posts': postagens,
        'form': form,
        'termo_busca': buscarHome if buscarHome else '',
    }
    return render(request, 'home.html', context)

# 💬 Página de Detalhes do Post (com comentários)
def detalhe_post(request, post_id):
    # Pega o post específico ou retorna 404
    post = get_object_or_404(Post, id=post_id)
    
    # Pega todos os feedbacks deste post, ordenados do mais recente
    feedbacks = post.feedbacks.all().order_by('-data_envio')
    
    # Processa novo comentário
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
    
    # Estatísticas dos comentários
    total_comentarios = feedbacks.count()
    
    context = {
        'post': post,
        'feedbacks': feedbacks,
        'form': form,
        'total_comentarios': total_comentarios,
    }
    return render(request, 'detalhe_post.html', context)

# 💬 Central de Comentários
def central_comentarios(request):
    todos_feedbacks = Feedback.objects.select_related('post', 'usuario').all().order_by('-data_envio')
    
    total_comentarios = todos_feedbacks.count()
    total_posts_comentados = Feedback.objects.values('post').distinct().count()
    usuarios_mais_ativos = Feedback.objects.values('usuario__username').annotate(
        total=Count('id')
    ).order_by('-total')[:5]
    
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
        'filtro': filtro,
    }
    return render(request, 'central_comentarios.html', context)

# 📁 Página de Documentos
def documents(request):
    documentos = Post.objects.exclude(arquivo='')
    return render(request, 'documents.html', {'documentos': documentos})

# 👤 Perfil
def profile_view(request):
    if request.user.is_authenticated:
        meus_comentarios = Feedback.objects.filter(usuario=request.user).select_related('post').order_by('-data_envio')
    else:
        meus_comentarios = []
    
    return render(request, 'perfil.html', {'meus_comentarios': meus_comentarios})

def login_view(request):
    return render(request, 'login.html')

def logout_view(request):
    return redirect('home')

def register_view(request):
    return render(request, 'register.html')