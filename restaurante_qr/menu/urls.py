from django.urls import path
from .views import *

urlpatterns = [
    path('producto/editar/<int:producto_id>/', editar_producto, name='editar_producto'),
    path('producto/eliminar/<int:producto_id>/', eliminar_producto, name='eliminar_producto'),
    path('producto/disponible/<int:producto_id>/', producto_diponible, name='producto_disponible'),
    path('gestionar/<int:restaurante_id>/', gestionar_menu, name='gestionar_menu'),
    path('categoria/editar/<int:categoria_id>/', editar_categoria, name='editar_categoria'),
    path('categoria/eliminar/<int:categoria_id>/', eliminar_categoria, name='eliminar_categoria'),
    path('categoria/subir/<int:categoria_id>/', subir_categoria, name='subir_categoria'),
    path('categoria/bajar/<int:categoria_id>/', bajar_categoria, name='bajar_categoria'),




]