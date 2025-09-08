from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

class Restaurante (models.Model):
    nombre = models.CharField (max_length=50)
    direccion = models.TextField(blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    email_contacto = models.EmailField(blank=True)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    horario_apertura = models.TimeField(blank=True, null=True)
    horario_cierre = models.TimeField(blank=True, null=True)
    propietario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='restaurantes')
    f_creacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nombre

class Mesa (models.Model):
    Ubicaciones= [
        ('interior', 'Interior'),
        ('exterior', 'Exterior'),
        ('barra', 'Barra'),
    ]
    restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE, related_name='mesas')
    numero= models.PositiveIntegerField()
    identificador_qr= models.UUIDField(default=uuid.uuid4, editable= False, unique=True)
    activa = models.BooleanField(default=True)
    ubicacion = models.CharField(max_length=20, choices=Ubicaciones, default='interior')
    orden = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"Mesa {self.numero} - {self.restaurante.nombre}"
    