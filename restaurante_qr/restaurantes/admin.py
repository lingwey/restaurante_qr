from django.contrib import admin
from .models import Restaurante, Mesa

@admin.register(Restaurante)
class RestauranteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'propietario', 'direccion', 'f_creacion')
    search_fields = ('nombre', 'direccion')

@admin.register(Mesa)
class MesaAdmin(admin.ModelAdmin):
    list_display = ('numero', 'restaurante', 'activa', 'identificador_qr')
    list_filter = ('activa', 'restaurante')
    search_fields = ('numero',)

