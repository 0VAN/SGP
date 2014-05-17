from django.db import models
from desarrollo.models import *
# Create your models here.

class LineBase(models.Model):
    Nombre = models.CharField(max_length=30)
    Fecha = models.DateTimeField(auto_now=True)
    Usuario = models.ForeignKey(User)
    Items = models.ManyToManyField(Item)
    Fase = models.ForeignKey(Fase)