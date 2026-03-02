from django.contrib import admin
from django.urls import path
from core import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    # ADMIN
    path('admin/', admin.site.urls),

    # AUTENTICAÇÃO
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),

    # PERFIL
    path('profile/', views.profile_view, name='profile'),
    path('perfil/', views.profile_view, name='perfil'),

    # PÁGINAS INSTITUCIONAIS
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),

    # DOCUMENTOS
    path('documents/', views.documents, name='documents'),

    # FATURAMENTO
    path('faturamento/', views.faturamento, name='faturamento'),

    # POSTS E COMENTÁRIOS
    path('post/<int:post_id>/', views.detalhe_post, name='detalhe_post'),
    path('comentarios/', views.central_comentarios, name='central_comentarios'),
]

# CONFIGURAÇÃO PARA ARQUIVOS MEDIA (UPLOADS)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)