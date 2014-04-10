
from django.db import models

# Create your models here.

class Usuario(models.Model):
    #Nombre_de_usuario = models.CharField(max_length=30)
    #Contrasena = models.CharField(max_length=20) # falta como hacer que la contrasenha este encriptada

    Nombres = models.CharField(max_length=50)
    Apellidos = models.CharField(max_length=50)
    Email = models.CharField(max_length=50)
    Direccion = models.CharField(max_length=100)
    Numero_de_telefono = models.CharField(max_length=50)
    Observacion = models.CharField(max_length=50)
    def __unicode__(self):
        return self.Nombre_de_usuario

