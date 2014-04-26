from django.db import models
from administracion.models import Fase, TipoDeItem
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