from django.db import models
from restaurantes.models import Restaurante

class Categoria(models.Model):
    nombre= models.CharField(max_length=100)
    restaurante= models.ForeignKey(Restaurante, on_delete=models.CASCADE)
    orden= models.PositiveIntegerField(default=0)
    
    class Meta:
        unique_together=('nombre', 'restaurante')
        ordering= ['orden']
        
    def __str__(self):
        return self.nombre
    
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion= models.TextField(blank=True)
    precio= models.DecimalField(max_digits=6, decimal_places=2)
    imagen= models.ImageField(upload_to='productos/',blank=True, null=True)
    disponible= models.BooleanField(default=True)
    orden= models.PositiveIntegerField(default=0)
    #relacion con categoria y restaurante
    categoria=models.ForeignKey(Categoria, on_delete=models.CASCADE, null=True, blank=True)
    restaurante=models.ForeignKey(Restaurante, on_delete=models.CASCADE)
    
    class Meta:
        ordering= ['orden']
        
    def __str__(self):
        return self.nombre


    
