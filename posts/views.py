from django.shortcuts import render, redirect, get_object_or_404
from .models import Post 
from .forms import FeedbackForm

# 🏠 Página Inicial: Lista posts e permite busca
def home(request):
    # 1. Lógica de Busca
    buscarHome = request.GET.get('campoBuscaHome')
    if buscarHome and buscarHome.strip():
        postagens = Post.objects.filter(titulo__icontains=buscarHome.strip())
    else:
        postagens = Post.objects.all()

    # 2. Lógica para processar feedback enviado pela Home (opcional)
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
    return render(request, 'home.html', {
        'posts': postagens,
        'form': form
    })

# 💬 Página de Detalhes: Mostra um post específico e seus feedbacks
def detalhe_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    feedbacks = post.feedbacks.all()
    
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

    return render(request, 'detalhe_post.html', {
        'post': post,
        'feedbacks': feedbacks,
        'form': form
    })

# 📁 Página de Documentos
def documents(request):
    documentos = Post.objects.exclude(arquivo='')
    return render(request, 'documents.html', {'documentos': documentos})

# 👤 Outras Views
def profile_view(request):
    return render(request, 'perfil.html')

def login_view(request):
    return render(request, 'login.html')

def logout_view(request):
    return redirect('home')

def register_view(request):
    return render(request, 'register.html')