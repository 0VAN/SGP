from django.db import models
from administracion.models import *
from django.contrib.auth.models import User, Group, Permission

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


    def __unicode__(self):
        return self.Nombre

class Campo(models.Model):
    item = models.ForeignKey(Item, null=True, blank=True)
    tipoItem = models.ForeignKey(TipoDeItem, null=True, blank=True)
    atributo = models.ForeignKey(Atributo, null=True, blank=True)
    fecha = models.DateField(null=True)
    numerico = models.DecimalField(max_digits=30, decimal_places=10, null=True)
    logico = models.NullBooleanField()
    cadena = models.CharField(max_length=50, blank=True)
    texto = models.TextField(blank=True)
    mail = models.EmailField(blank=True, null=True)
    hora = models.TimeField(blank=True, null=True)

class Logico(models.Model):
    dato = models.BooleanField(default=False)


class Logico1(models.Model):
    dato = models.NullBooleanField()