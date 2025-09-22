from django.urls import path
from .views import *

urlpatterns = [
    path('producto/editar/<int:producto_id>/', editar_producto, name='editar_producto'),
    path('producto/eliminar/<int:producto_id>/', eliminar_producto, name='eliminar_producto'),
    path('gestionar/<int:restaurante_id>/', gestionar_menu, name='gestionar_menu'),


]