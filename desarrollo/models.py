from django.db import models
from administracion.models import *
from django.contrib.auth.models import User, Group, Permission

# Create your models here.


class TipoAtributo(models.Model):
    Nombre = models.CharField(max_length=30)
    Tipo = models.CharField(max_length=1)

    def __unicode__(self):
        return self.Nombre


class Numerico(TipoAtributo):
    Dato = models.IntegerField()


class Fecha(TipoAtributo):
    Dato = models.DateField()


class Hora(TipoAtributo):
    Dato = models.TimeField()


class Logico(TipoAtributo):
    Dato = models.BooleanField()


class Mail(TipoAtributo):
    Dato = models.EmailField()


class Texto(TipoAtributo):
    Dato = models.TextField()


class Cadena(TipoAtributo):
    Dato = models.CharField(max_length=100)



class Item(models.Model):

    CONSTRUCCION = 'CON'
    VALIDADO = 'VAL'
    FINALIZADO = 'FIN'
    REVISION = 'REV'
    ESTADO_CHOICES = (
        (CONSTRUCCION, 'Construccion'),
        (VALIDADO, 'Validado'),
        (FINALIZADO, 'Finalizado'),
        (REVISION, 'Revision'),
    )

    Nombre = models.CharField(max_length=30, unique=True)
    Descripcion = models.TextField(blank=True)
    Prioridad = models.IntegerField(max_length=3, blank=False)
    CostoTemporal = models.IntegerField(blank=False)
    CostoUnitario = models.IntegerField(blank=False)
    Estado = models.CharField(max_length=3, choices=ESTADO_CHOICES, default=CONSTRUCCION)
    Usuario = models.ForeignKey(User)
    Fecha = models.DateTimeField(auto_now=True)
    Fase = models.ForeignKey(Fase)
    Tipo = models.ForeignKey(TipoDeItem)
    Version = models.IntegerField()
    Observacion = models.TextField(blank=True)
    Campos = models.ManyToManyField(TipoAtributo)



    def __unicode__(self):
        return self.Nombre

