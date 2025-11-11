from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import *
from .forms import *

@login_required
def crear_restaurante(request):
    if request.user.rol != 'propietario':
        return HttpResponseForbidden("No tenés permiso para crear restaurantes.")
    form= RestauranteForms(request.POST or None, request.FILES or None)
    if form.is_valid():
        restaurante = form.save(commit= False)
        restaurante.propietario = request.user
        #url = subir_imagen_a_supabase(imagen, carpeta=f"logos/restaurante_{restaurante.id}")
        restaurante.save()
        return redirect('restaurantes:editar_restaurante', restaurante.id)
    return render (request, 'restaurantes/crear_restaurante.html', {'form': form})

@login_required
def crear_mesa(request, restaurante_id):
    restaurante = get_object_or_404(Restaurante, id= restaurante_id, propietario = request.user)
    form = MesaForms(request.POST or None)
    if form.is_valid():
        mesa= form.save(commint= False)
        mesa.restaurante = restaurante
        mesa.save()
        return redirect('restaurantes:editar_restaurante',restaurante.id)
    return render(request,'restaurante/crear_mesa.html',{'form':form, 'restaurante':restaurante})

@login_required
def editar_restaurante(request, restaurante_id):
    restaurante= get_object_or_404(Restaurante, id= restaurante_id, propietario= request.user)
    form = RestauranteForms(request.POST or None, request.FILES or None, instance=restaurante)
    if form.is_valid():
        form.save()
        return redirect('restaurantes:editar_restaurtante', restaurante_id)
    return render (request, 'restaurantes/editar_restaurante.html',{'form': form, 'restaurante':restaurante})

@login_required
def editar_mesa(request, mesa_id):
    mesa = get_object_or_404(Mesa, id= mesa_id, restaurante__propietario= request.user)
    form = MesaForms(request.POST or None, instance=mesa)
    if form.is_valid():
        form.save()
        return redirect ('restaurantes:editar_restaurante', mesa.restaurante.id)
    return render (request, 'restaurantes/editar_mesa.html',{'form': form, 'mesa':mesa})
    
