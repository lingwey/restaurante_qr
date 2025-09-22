from django import forms
from .models import *

class RestauranteForms(forms.ModelForm):
    class Meta:
        model= Restaurante
        fields = ['nombre','direccion','telefono','email_contacto','logo' ]

class MesaForms(forms.ModelForm):
    class Meta:
        model= Mesa
        fields= ['numero','ubicacion','activa','orden']
    