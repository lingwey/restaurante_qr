from django import forms
from django.db.models import Max
from .models import Categoria, Producto

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Ej: Pastas, Bebidas, Postres'}),
        }

    def __init__(self, *args, **kwargs):
        self.restaurante = kwargs.pop('restaurante', None)
        super().__init__(*args, **kwargs)

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        if Categoria.objects.filter(nombre__iexact=nombre, restaurante=self.restaurante).exists():
            raise forms.ValidationError("Ya existe una categoría con ese nombre en este restaurante.")
        return nombre

    def save(self, commit=True):
        nueva_categoria = super().save(commit=False)
        nueva_categoria.restaurante = self.restaurante

        if nueva_categoria.orden == 0:
            ultimo = Categoria.objects.filter(restaurante=self.restaurante).aggregate(Max('orden'))['orden__max'] or 0
            nueva_categoria.orden = ultimo + 1

        if commit:
            nueva_categoria.save()
        return nueva_categoria


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'imagen', 'categoria', 'disponible']
        
    #crea el apartado del selector de categorias usando lo creado en el CategoriaForm
    def __init__(self, *args, **kwargs):
        restaurante = kwargs.pop('restaurante', None)
        super().__init__(*args, **kwargs)

        if restaurante:
            self.fields['categoria'].queryset = Categoria.objects.filter(restaurante=restaurante)
