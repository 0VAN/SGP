
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

"""
    Se utiliza la clase User por de defecto en Django para la creacion de los usuarios, pero
    se incluyen 3 atributos:
        - direccion: direccion del usuario
        - telefono: numero del telefono del usuario
        - observacion: observacion sobre el usuario por parte del administrador del sistema


"""

User.add_to_class('direccion', models.FloatField(null=True, blank=True))
User.add_to_class('telefono', models.PositiveIntegerField(null=True, blank=True))
User.add_to_class('observacion', models.PositiveIntegerField(null=True, blank=True))


class Proyecto(models.Model):
    Nombre_del_Proyecto = models.CharField(max_length=30, unique=True)
    Descripcion_del_Proyecto= models.TextField
    Fecha_de_inicio = models.DateField
    Fecha_de_finalizacion = models.DateField
