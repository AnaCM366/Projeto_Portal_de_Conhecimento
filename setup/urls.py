from django.contrib import admin
from django.urls import path
from core.views import home
from django.contrib.auth import views as auth_views

urlpatterns = [
    # ADMIN
    path('admin/', admin.site.urls),

    # HOME
    path('', home, name='home'),

    # LOGIN
    path('login/', auth_views.LoginView.as_view(
        template_name='registration/login.html'
    ), name='login'),

    # LOGOUT
    path('logout/', auth_views.LogoutView.as_view(
        next_page='login'
    ), name='logout'),
]