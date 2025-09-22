from django.urls import path
from .views import *

app_name= 'usuarios'

urlpatterns = [
    path('registro/', registro_usuario, name='registro_usuario'),
    path('registro/completar/', completar_datos_mozo, name='completar_datos_mozo'),
    path('registro/', registro_usuario, name='registro_usuario'),
    path('dashboard/propietario/', dashboard_propietario, name='dashboard_propietario'),
    path('dashboard/mozo/', dashboard_mozo, name='dashboard_mozo'),
    path('dashboard/', dashboard, name='dashboard'),



]