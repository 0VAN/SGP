from django.db import models
from administracion.models import *
from django.contrib.auth.models import User, Group, Permission
import reversion

# Create your models here.



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
    Descripcion = models.TextField()
    Prioridad = models.IntegerField(max_length=3, blank=False)
    CostoTemporal = models.IntegerField(blank=False)
    CostoUnitario = models.IntegerField(blank=False)
    Estado = models.CharField(max_length=3, choices=ESTADO_CHOICES, default=CONSTRUCCION)
    Usuario = models.ForeignKey(User)
    Fecha = models.DateTimeField(auto_now=True)
    Fase = models.ForeignKey(Fase)
    Tipo = models.ForeignKey(TipoDeItem)
    Version = models.IntegerField()

    def __unicode__(self):
        return self.Nombre

reversion.register(Item)

class Campo(models.Model):
    item = models.ForeignKey(Item, null=True, blank=True)
    tipoItem = models.ForeignKey(TipoDeItem, null=True, blank=True)
    atributo = models.ForeignKey(Atributo, null=True, blank=True)
    fecha = models.DateField(null=True)
    numerico = models.DecimalField(null=True, decimal_places=3, max_digits=10, blank=True)
    longitud = models.IntegerField(null=True)
    precision = models.IntegerField(null=True)
    logico = models.NullBooleanField()
    cadena = models.CharField(blank=True, null=True, max_length=500)
    mail = models.EmailField(blank=True, null=True)
    hora = models.TimeField(blank=True, null=True)


class Relacion(models.Model):
    padre = models.ForeignKey(Item, null=True, related_name='padre')
    antecesor = models.ForeignKey(Item, null=True, related_name='antecesor')
    item = models.ForeignKey(Item, null=True, related_name='item')