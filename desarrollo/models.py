from django.db import models
from administracion.models import Fase, Proyecto, Atributo, TipoDeItem
from django.contrib.auth.models import User
import reversion

# Create your models here.



class Item(models.Model):

    CONSTRUCCION = 'CON'
    VALIDADO = 'VAL'
    FINALIZADO = 'FIN'
    REVISION = 'REV'
    SOLICITUD = 'SOL'
    CREDENCIAL = 'CRE'
    ESTADO_CHOICES = (
        (CONSTRUCCION, 'Construccion'),
        (VALIDADO, 'Validado'),
        (FINALIZADO, 'Aprobado'),
        (REVISION, 'Revision'),
        (SOLICITUD, 'En solicitud de cambio'),
        (CREDENCIAL, 'En credencial'),
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
    ACTIVO = 'A'
    ELIMINADO = 'E'

    CONDICION_CHOICES = (
        (ACTIVO, 'Activo'),
        (ELIMINADO, 'Eliminado'),
    )
    condicion = models.CharField(max_length=1, choices=CONDICION_CHOICES, default=ACTIVO)

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


reversion.register(Campo)

class Relacion(models.Model):
    padre = models.ForeignKey(Item, null=True, related_name='padre',on_delete=models.SET_NULL)
    antecesor = models.ForeignKey(Item, null=True, related_name='antecesor',on_delete=models.SET_NULL)
    item = models.ForeignKey(Item, null=True, related_name='item')
    ACTIVO = 'A'
    ELIMINADO = 'E'

    ESTADO_CHOICES = (
        (ACTIVO, 'Activa'),
        (ELIMINADO, 'Inactiva'),
    )
    estado = models.CharField(max_length=1, choices=ESTADO_CHOICES, default=ELIMINADO)

    def estado_padre(self):
        if self.padre:
            if self.padre.condicion == 'A':
                return True
        return False

    def estado_antecesor(self):
        if self.antecesor:
            if self.antecesor.condicion == "A":
                return True
        return False

reversion.register(Relacion)

class Archivo(models.Model):
    archivo = models.FileField(upload_to='carga')
    item = models.ForeignKey(Item)
    #nombre = models.CharField(max_length=30)

    def __unicode__(self):
        return self.archivo

reversion.register(Archivo)
