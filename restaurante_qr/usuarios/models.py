from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    ROLES = (
        ('propietario', 'Propietario'),
        ('mozo', 'Mozo'),
    )
    rol = models.CharField(max_length=20, choices=ROLES)
    validado_por_propietario = models.BooleanField(default=False)
