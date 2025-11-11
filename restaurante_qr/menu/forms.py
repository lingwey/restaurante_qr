from django import forms
from django.forms import modelformset_factory 
from django.db.models import Max
from .models import Categoria, Producto, RangoHorario

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
    imagen=forms.ImageField(required=False)
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'categoria', 'disponible']
    
    def clean_imagen(self):
        imagen_archivo = self.cleaned_data.get('imagen')
        if imagen_archivo is None:
             return None  
        return imagen_archivo
        
    #crea el apartado del selector de categorias usando lo creado en el CategoriaForm
    def __init__(self, *args, **kwargs):
        restaurante = kwargs.pop('restaurante', None)
        super().__init__(*args, **kwargs)

        if restaurante:
            self.fields['categoria'].queryset = Categoria.objects.filter(restaurante=restaurante)


class RangoHorarioForm(forms.ModelForm):
    class Meta:
        model = RangoHorario
        fields = [ 'hora_inicio', 'hora_fin']
        widgets = {
            'hora_inicio': forms.TimeInput(attrs={'type': 'time'}),
            'hora_fin': forms.TimeInput(attrs={'type': 'time'}),
        }
        
    def __init__(self, *args, **kwargs):
        self.categoria = kwargs.pop('categoria', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        inicio = cleaned_data.get('hora_inicio')
        fin = cleaned_data.get('hora_fin')
        
        if inicio and fin and inicio >= fin:
            raise forms.ValidationError('La hora de inicio debe ser menor que la hora final.')
        
        if self.categoria and self.categoria.rangos_horarios.count() >= 3:
            raise forms.ValidationError('Esta categoría ya tiene el máximo de horarios asignados.')
        return cleaned_data
        

def get_rango_horario_formset(extra=1):
    return modelformset_factory(
        RangoHorario,
        fields=('hora_inicio', 'hora_fin'),
        extra=extra,
        max_num=1,
        widgets={
            'hora_inicio': forms.TimeInput(attrs={'type': 'time'}),
            'hora_fin': forms.TimeInput(attrs={'type': 'time'}),
        }
    )
