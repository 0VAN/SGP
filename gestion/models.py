from django.db import models
from desarrollo.models import Item
from administracion.models import User, Proyecto, Fase
# Create your models here.

class LineaBase(models.Model):
    Nombre = models.CharField(max_length=30)
    Fecha = models.DateTimeField(auto_now=True)
    Usuario = models.ForeignKey(User)
    Items = models.ManyToManyField(Item)
    Fase = models.ForeignKey(Fase)

class ComiteDeCambio(models.Model):
    Miembros = models.ManyToManyField(User)
    Proyecto = models.ForeignKey(Proyecto)


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

    def __unicode__(self):
        return self.nombre



class Voto(models.Model):
    solicitud = models.ForeignKey(SolicitudCambio)
    usuario = models.ForeignKey(User)
    PROCESO = 'P'
    ACEPTADO = 'A'
    RECHAZADO = 'R'
    ESTADO_CHOICES = (
        (PROCESO, 'En proceso'),
        (ACEPTADO, 'Aceptado'),
        (RECHAZADO, 'Rechazado'),
    )
    estado = models.CharField(max_length=1, choices=ESTADO_CHOICES, default=PROCESO)


class Credencial(models.Model):
    solicitud = models.ForeignKey(SolicitudCambio)
    fechaCreacion = models.DateField(auto_now_add=True, verbose_name='Fecha de creacion')
    fechaFinalizacion = models.DateField(verbose_name='Fecha de finalizacion')

    def __unicode__(self):
        return 'Credencial de la solicitud aprobada: ' + self.solicitud.nombre
