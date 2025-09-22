from django import forms
from .models import Categoria, Producto

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'orden']
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
        categoria = super().save(commit=False)
        categoria.restaurante = self.restaurante
        if commit:
            categoria.save()
        return categoria

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
