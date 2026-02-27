from django.shortcuts import render, redirect
from .models import Post 

# 🏠 Página Inicial com Filtro de Busca
def home(request):
    buscarHome = request.GET.get('campoBuscaHome')
    
    if buscarHome and buscarHome.strip():
        postagens = Post.objects.filter(titulo__icontains=buscarHome.strip())
    else:
        postagens = Post.objects.all()
    
    return render(request, 'home.html', {'posts': postagens})

# 📁 Página de Documentos
def documents(request):
    # Aqui você pode buscar apenas posts que tenham arquivos, por exemplo
    documentos = Post.objects.exclude(arquivo='')
    return render(request, 'documents.html', {'documentos': documentos})

# 👤 Página de Perfil (Usada para 'profile' e 'perfil')
def profile_view(request):
    return render(request, 'perfil.html')

# 🔐 Autenticação (Login/Logout/Register)
def login_view(request):
    return render(request, 'login.html')

def logout_view(request):
    # Por enquanto apenas redireciona para a home
    return redirect('home')

def register_view(request):
    return render(request, 'register.html')