from django.contrib import admin
from django.urls import path
from core import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('documents/', views.documents, name='documents'),
    path('perfil/', views.profile_view, name='perfil'),
    
    # NOVAS URLs para o sistema de comentários
    path('post/<int:post_id>/', views.detalhe_post, name='detalhe_post'),
    path('comentarios/', views.central_comentarios, name='central_comentarios'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)