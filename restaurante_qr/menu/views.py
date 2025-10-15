from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from restaurantes.models import Restaurante
from .forms import CategoriaForm, ProductoForm, RangoHorarioForm, get_rango_horario_formset
from .models import Categoria, Producto, RangoHorario
from django.contrib import messages

@login_required
def crear_menu(request, restaurante_id):
    restaurante = Restaurante.objects.get(id=restaurante_id)
    return render(request, 'menu/crear_menu.html', {'restaurante': restaurante})

@login_required
def editar_menu(request, restaurante_id):
    restaurante = Restaurante.objects.get(id=restaurante_id)
    return render(request, 'menu/editar_menu.html', {'restaurante': restaurante})

@login_required
def gestionar_menu(request, restaurante_id):
    restaurante = get_object_or_404(Restaurante, id=restaurante_id, propietario=request.user)
    categorias = Categoria.objects.filter(restaurante=restaurante).prefetch_related('producto_set')
    editar_horario_id = request.GET.get('editar_rango_horario')

    categoria_form = CategoriaForm(request.POST or None, restaurante=restaurante, prefix='cat')
    producto_form = ProductoForm(request.POST or None, request.FILES or None, restaurante=restaurante, prefix='producto')

    formsets_por_categoria = {}
    horarios_editables = []

    # Procesamiento de formularios
    if request.method == 'POST':
        if 'cat-nombre' in request.POST:
            if categoria_form.is_valid():
                categoria_form.save()
                return redirect(request.path)

        elif 'producto-nombre' in request.POST:
            if producto_form.is_valid():
                plato = producto_form.save(commit=False)
                plato.restaurante = restaurante
                plato.save()
                return redirect(request.path)

        elif 'rango_categoria_id' in request.POST:
            categoria_id = request.POST.get('rango_categoria_id')
            if not categoria_id:
                messages.error(request, "No se recibió el ID de categoría.")
                return redirect(request.path)

            categoria_obj = get_object_or_404(Categoria, id=int(categoria_id), restaurante=restaurante)
            prefix = f"horario_{categoria_id}"

            cantidad_existente = categoria_obj.rangos_horarios.count()
            cantidad_restante = max(0, 2 - cantidad_existente)

            FormSet = get_rango_horario_formset(extra=cantidad_restante)
            formset = FormSet(request.POST, queryset=RangoHorario.objects.none(), prefix=prefix)

            if formset.is_valid():
                for form in formset:
                    if form.cleaned_data:
                        nuevo_rango = form.save(commit=False)
                        nuevo_rango.restaurante = restaurante
                        nuevo_rango.categoria = categoria_obj
                        nuevo_rango.save()
                return redirect(request.path)

    # Formularios de edición por horario
    for categoria in categorias:
        for horario in categoria.rangos_horarios.all():
            form = RangoHorarioForm(instance=horario)
            horarios_editables.append({
                'horario': horario,
                'form': form,
                'categoria_id': categoria.id,
            })

    # Formsets dinámicos por categoría (flujo GET)
    for categoria in categorias:
        cantidad_existente = categoria.rangos_horarios.count()
        cantidad_restante = max(0, 2 - cantidad_existente)

        prefix = f"horario_{categoria.id}"
        FormSet = get_rango_horario_formset(extra=cantidad_restante)
        formset = FormSet(queryset=RangoHorario.objects.none(), prefix=prefix)
        formsets_por_categoria[categoria.id] = formset

    return render(request, 'menu/gestionar_menu.html', {
        'restaurante': restaurante,
        'categoria_form': categoria_form,
        'producto_form': producto_form,
        'categorias': categorias,
        'editar_horario_id': editar_horario_id,
        'horarios_editables': horarios_editables,
        'formsets_por_categoria': formsets_por_categoria,
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

@login_required
def producto_diponible(request, producto_id):
    producto=get_object_or_404(Producto, id=producto_id, restaurante__propietario=request.user)
    producto.disponible= not producto.disponible
    producto.save()
    return redirect('menu:gestionar_menu', restaurante_id=producto.restaurante.id)

@login_required
def editar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id, restaurante__propietario=request.user)

    if request.method == 'POST':
        nuevo_nombre = request.POST.get('nombre')
        if nuevo_nombre:
            categoria.nombre = nuevo_nombre
            categoria.save()
    return redirect('menu:gestionar_menu', restaurante_id=categoria.restaurante.id)

@login_required
def eliminar_categoria(request, categoria_id):
    categoria= get_object_or_404(Categoria, id=categoria_id, restaurante__propietario=request.user)
    restaurante_id = categoria.restaurante.id
    categoria.delete()
    return redirect('menu:gestionar_menu', restaurante_id=restaurante_id)

@login_required
def subir_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id, restaurante__propietario=request.user)
    anterior = Categoria.objects.filter(
        restaurante=categoria.restaurante,
        orden__lt=categoria.orden
    ).order_by('-orden').first()

    if anterior:
        categoria.orden, anterior.orden = anterior.orden, categoria.orden
        categoria.save()
        anterior.save()

    return redirect('menu:gestionar_menu', restaurante_id=categoria.restaurante.id)

@login_required
def bajar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id, restaurante__propietario=request.user)
    siguiente = Categoria.objects.filter(
        restaurante=categoria.restaurante,
        orden__gt=categoria.orden
    ).order_by('orden').first()

    if siguiente:
        categoria.orden, siguiente.orden = siguiente.orden, categoria.orden
        categoria.save()
        siguiente.save()

    return redirect('menu:gestionar_menu', restaurante_id=categoria.restaurante.id)
@login_required
def elimanr_rango_horario(request, horario_id):
    rango_horario= get_object_or_404(RangoHorario, id=horario_id, restaurante__propietario=request.user)
    restaurante_id= rango_horario.restaurante.id
    rango_horario.delete()
    messages.success(request, "horario eliminado correctamente")
    return redirect('menu:gestionar_menu', restaurante_id= restaurante_id)

@login_required
def editar_rango_horario(request, horario_id):
    rango_horario= get_object_or_404(RangoHorario, id= horario_id, restaurante__propietario= request.user)
    form= RangoHorarioForm(request.POST or None, instance= rango_horario, categoria=rango_horario.categoria)
    if form.is_valid():
        form.save()
        messages.success(request, 'horario cambiado')
        return redirect('menu:gestionar_menu', restaurante_id=rango_horario.restaurante.id)
