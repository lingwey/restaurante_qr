from django import forms
from django.contrib.auth.forms import UserCreationForm
from usuarios.models import Usuario
from restaurantes.models import Restaurante, MozoAsignado

class RegistroUsuarioForm(UserCreationForm):
    rol = forms.ChoiceField(choices=Usuario.ROLES, label="Rol")

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password1', 'password2', 'rol']

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.rol = self.cleaned_data['rol']

        if usuario.rol == 'mozo':
            usuario.validado_por_propietario = False

        if commit:
            usuario.save()
        return usuario


class CompletarDatosMozoForm(forms.Form):
    nombre_restaurante = forms.CharField(label="Nombre del restaurante")
    foto = forms.ImageField(required=False)

    def clean_nombre_restaurante(self):
        nombre = self.cleaned_data['nombre_restaurante']
        try:
            return Restaurante.objects.get(nombre__iexact=nombre)
        except Restaurante.DoesNotExist:
            raise forms.ValidationError("Ese restaurante no está registrado.")
