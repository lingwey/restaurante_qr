from django.urls import path
from . import views

app_name='restaurantes'

urlpatterns = [
    path('crear/', views.crear_restaurante, name='crear_restaurante'),
    path('<int:restaurante_id>/editar/', views.editar_restaurante, name='editar_restaurante'),
    path('<int:restaurante_id>/mesas/crear/', views.crear_mesa, name='crear_mesa'),
    path('mesas/<int:mesa_id>/editar/', views.editar_mesa, name='editar_mesa'),
    ]
