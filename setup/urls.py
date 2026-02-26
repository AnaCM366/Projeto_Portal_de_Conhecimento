from django.contrib import admin
from django.urls import path
from core import views
# from documents import views as DocumetoView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),  # You'll need to create these
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('documents/', views.documents, name='documents'),
    path('perfil/', views.profile_view, name='perfil'),

    
    # path('documentsNovo/', DocumetoView.documentos, name='documentos'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)