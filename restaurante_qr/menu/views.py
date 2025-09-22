from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from restaurantes.models import Restaurante
from .forms import CategoriaForm, ProductoForm
from .models import Categoria, Producto

def crear_menu(request, restaurante_id):
    restaurante = Restaurante.objects.get(id=restaurante_id)
    return render(request, 'menu/crear_menu.html', {'restaurante': restaurante})

def editar_menu(request, restaurante_id):
    restaurante = Restaurante.objects.get(id=restaurante_id)
    return render(request, 'menu/editar_menu.html', {'restaurante': restaurante})

@login_required
def gestionar_menu(request, restaurante_id):
    restaurante = get_object_or_404(Restaurante, id=restaurante_id, propietario=request.user)
    categorias = Categoria.objects.filter(restaurante=restaurante).prefetch_related('producto_set')
    
    categoria_form = CategoriaForm(request.POST or None, restaurante=restaurante, prefix='cat')
    producto_form = ProductoForm(request.POST or None, request.FILES or None, restaurante=restaurante, prefix='producto')

    if request.method == 'POST':
        if 'cat-nombre' in request.POST:  # detecta si se envió el form de categoria
            if categoria_form.is_valid():
                categoria_form.save()
                return redirect(request.path)
        elif 'producto-nombre' in request.POST:  # detecta si se envió el form de producto
            if producto_form.is_valid():
                plato = producto_form.save(commit=False)
                plato.restaurante = restaurante
                plato.save()
                return redirect(request.path)

    return render(request, 'menu/gestionar_menu.html', {
        'restaurante': restaurante,
        'categoria_form': categoria_form,
        'producto_form': producto_form,
        'categorias': categorias,
    })

@login_required
def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id, restaurante__propietario=request.user)
    form = ProductoForm(request.POST or None, request.FILES or None, instance=producto, restaurante=producto.restaurante)

    if form.is_valid():
        form.save()
        return redirect('menu:gestionar_menu', restaurante_id=producto.restaurante.id)

    return render(request, 'menu/editar_producto.html', {'form': form, 'producto': producto})

@login_required
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id, restaurante__propietario=request.user)
    restaurante_id = producto.restaurante.id
    producto.delete()
    return redirect('menu:gestionar_menu', restaurante_id=restaurante_id)
