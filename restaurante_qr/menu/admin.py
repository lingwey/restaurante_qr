from django.contrib import admin
from .models import Producto, Categoria

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'precio', 'categoria', 'disponible', 'imagen']
    list_filter = ['categoria', 'disponible']
    search_fields = ['nombre', 'descripcion']
    readonly_fields = ['imagen']  # si querés evitar edición directa

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'restaurante']
    list_filter = ['restaurante']
    search_fields = ['nombre']
