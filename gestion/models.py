from django.db import models
from desarrollo.models import *
from administracion.models import *
# Create your models here.

class LineBase(models.Model):
    Nombre = models.CharField(max_length=30)
    Fecha = models.DateTimeField(auto_now=True)
    Usuario = models.ForeignKey(User)
    Items = models.ManyToManyField(Item)
    Fase = models.ForeignKey(Fase)

class ComiteDeCambio(models.Model):
    Usuario1 = models.ForeignKey(User, related_name="Usuario1")
    Usuario2 = models.ForeignKey(User, related_name="Usuario2")
    Usuario3 = models.ForeignKey(User, related_name="Usuario3")
    Proyecto = models.ForeignKey(Proyecto)