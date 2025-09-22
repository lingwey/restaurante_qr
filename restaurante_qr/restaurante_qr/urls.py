from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('restaurantes/', include('restaurantes.urls', namespace='restaurantes')),
    path('usuarios/', include('usuarios.urls', namespace='usuarios')),
    path('menu/', include(('menu.urls', 'menu'), namespace='menu')),
    path('login/', auth_views.LoginView.as_view(template_name='usuarios/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]