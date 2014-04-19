
from django.db import models
from django.contrib.auth.models import User, Group, Permission

# Create your models here.
"""
    Se utiliza la clase User por de defecto en Django para la creacion de los usuarios, pero
    se incluyen 3 atributos:
        - direccion: direccion del usuario
        - telefono: numero del telefono del usuario
        - observacion: observacion sobre el usuario por parte del administrador del sistema

"""

User.add_to_class('direccion', models.TextField(null=True, blank=True))
User.add_to_class('telefono', models.PositiveIntegerField(null=True, blank=True))
User.add_to_class('observacion', models.TextField(null=True, blank=True))


class Proyecto(models.Model):
    Lider_del_Proyecto = models.ForeignKey(User)
    Nombre_del_Proyecto = models.CharField(max_length=30, unique=True)
    Descripcion_del_Proyecto = models.TextField()
    Fecha_inicio = models.DateField('Fecha de inicio')
    Fecha_finalizacion = models.DateField('Fecha de finalizacion')

class Fase(models.Model):
    Nombre = models.CharField(max_length=50)
    Descripcion = models.TextField()
    Usuario = models.ForeignKey(User)
    Fecha = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.Nombre

def tienePermiso(self, permiso):
    for grupo in self.groups.all():
        for permisoUsuario in grupo.permissions.all():
            if permisoUsuario.codename == permiso:
                return True
    return False

User.add_to_class('tienePermiso', tienePermiso)

def accesoAdministracion(self):
    rol ='Administracion'
    for grupo in self.groups.all():
        if grupo.name == rol:
            return True
    return False

User.add_to_class('accesoAdministracion', accesoAdministracion)

#Rol administracion
grupoAdministracion, created = Group.objects.get_or_create(name='Administracion')
if created:
    grupoAdministracion.save()
    #permisos de Proyecto
permisoAdd = Permission.objects.get(codename='add_proyecto')
permisoChange = Permission.objects.get(codename='change_proyecto')
permisoDelete = Permission.objects.get(codename='delete_proyecto')
grupoAdministracion.permissions.add(permisoAdd, permisoChange, permisoDelete)
    #permisos de Usuario
permisoAdd = Permission.objects.get(codename='add_user')
permisoChange = Permission.objects.get(codename='change_user')
permisoDelete = Permission.objects.get(codename='delete_user')
grupoAdministracion.permissions.add(permisoAdd, permisoChange, permisoDelete)
    #permisos de Roles
permisoAdd = Permission.objects.get(codename='add_group')
permisoChange = Permission.objects.get(codename='change_group')
permisoDelete = Permission.objects.get(codename='delete_group')
grupoAdministracion.permissions.add(permisoAdd, permisoChange, permisoDelete)


    #Rol lider de Proyecto
grupoLiderProyecto, created = Group.objects.get_or_create(name='Lider de Proyecto')
if created:
    grupoLiderProyecto.save()
permisoAdd = Permission.objects.get(codename='add_fase')
permisoChange = Permission.objects.get(codename='change_fase')
permisoDelete = Permission.objects.get(codename='delete_fase')
grupoLiderProyecto.permissions.add(permisoAdd, permisoChange, permisoDelete)
