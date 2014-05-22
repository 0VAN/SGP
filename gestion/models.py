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
    def __unicode__(self):
        return self.Nombre


class SolicitudCambio(models.Model):
    nombre = models.CharField(max_length=50)
    usuario = models.ForeignKey(User)
    items = models.ManyToManyField(Item)
    fase = models.ForeignKey(Fase)
    proyecto = models.ForeignKey(Proyecto)
    motivo = models.TextField(verbose_name="Motivo de la solicitud")
    fecha = models.DateTimeField(auto_now_add=True)
    PROCESO = 'P'
    ACEPTADA = 'A'
    RECHAZADA = 'R'
    ESTADO_CHOICES = (
        (PROCESO, 'En proceso'),
        (ACEPTADA, 'Aceptada'),
        (RECHAZADA, 'Rechazada'),
    )
    estado = models.CharField(max_length=1, choices=ESTADO_CHOICES, default=PROCESO)
