from django.shortcuts import render, redirect
from .forms import RegistroUsuarioForm, CompletarDatosMozoForm
from restaurantes.models import MozoAsignado
from django.contrib.auth.decorators import login_required
from restaurantes.models import Restaurante, MozoAsignado, Mesa

def registro_usuario(request):
    form = RegistroUsuarioForm(request.POST or None)
    if form.is_valid():
        usuario = form.save()
        if usuario.rol == 'propietario':
            return redirect('restaurantes:crear_restaurante')
        elif usuario.rol == 'mozo':
            return redirect('usuarios:completar_datos_mozo')
    return render(request, 'usuarios/registro.html', {'form': form})

@login_required
def completar_datos_mozo(request):
    usuario = request.user

    if usuario.rol != 'mozo':
        return redirect('home')  # o algún error 403 personalizado

    if MozoAsignado.objects.filter(usuario=usuario).exists():
        return redirect('usuarios:registro_exitoso_mozo')  # ya completó los datos

    form = CompletarDatosMozoForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        restaurante = form.cleaned_data['nombre_restaurante']
        foto = form.cleaned_data.get('foto')
        #url = subir_imagen_a_supabase(imagen, carpeta=f"perfil/usuario_{usuario.id}")
        MozoAsignado.objects.create(
            usuario=usuario,
            restaurante=restaurante,
            foto=foto,
            validado=False
        )
        return redirect('usuarios:registro_exitoso_mozo')

    return render(request, 'usuarios/completar_datos_mozo.html', {'form': form})

@login_required
def dashboard(request):
    usuario = request.user

    if usuario.rol == 'propietario':
        tiene_restaurantes = Restaurante.objects.filter(propietario=usuario).exists()
        if tiene_restaurantes:
            return redirect('usuarios:dashboard_propietario')
        else:
            return redirect('restaurantes:crear_restaurante')

    elif usuario.rol == 'mozo':
        return redirect('usuarios:dashboard_mozo')
    print("👤 Usuario autenticado:", request.user.is_authenticated)
    print("👤 Usuario:", request.user)
    return redirect('home')
    
@login_required
def dashboard_propietario(request):
    usuario = request.user
    restaurantes = Restaurante.objects.filter(propietario=usuario)
    restaurante_id = request.GET.get('restaurante')
    restaurante_activo = None
    mozos = mesas = []
    print("👤 Usuario autenticado:", request.user.is_authenticated)
    print("👤 Usuario:", request.user)
    if restaurante_id:
        try:
            restaurante_activo = restaurantes.get(id=restaurante_id)
            mozos = MozoAsignado.objects.filter(restaurante=restaurante_activo)
            mesas = Mesa.objects.filter(restaurante=restaurante_activo)
        except Restaurante.DoesNotExist:
            pass

    return render(request, 'usuarios/dashboard_propietario.html', {
        'restaurantes': restaurantes,
        'restaurante_activo': restaurante_activo,
        'mozos': mozos,
        'mesas': mesas,
    })

@login_required
def dashboard_mozo(request):
    usuario = request.user
    try:
        asignacion = MozoAsignado.objects.get(usuario=usuario)
        mesas = Mesa.objects.filter(restaurante=asignacion.restaurante)
    except MozoAsignado.DoesNotExist:
        mesas = []

    return render(request, 'usuarios/dashboard_mozo.html', {
        'mesas': mesas,
    })
