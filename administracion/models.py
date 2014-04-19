
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
#Group.add_to_class('Usuario', models.ForeignKey(User))


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

def can_add_user(self):
    permiso = 'add_user'
    return self.tienePermiso(permiso)
User.add_to_class('can_add_user', can_add_user)

def can_add_proyecto(self):
    permiso = 'add_proyecto'
    return self.tienePermiso(permiso)
User.add_to_class('can_add_proyecto', can_add_proyecto)

def can_add_fase(self):
    permiso = 'add_fase'
    return self.tienePermiso(permiso)
User.add_to_class('can_add_fase', can_add_fase)

def can_add_group(self):
    permiso = 'add_group'
    return self.tienePermiso(permiso)
User.add_to_class('can_add_group', can_add_group)

def can_change_user(self):
    permiso = 'change_user'
    return self.tienePermiso(permiso)
User.add_to_class('can_change_user', can_change_user)

def can_change_proyecto(self):
    permiso = 'change_proyecto'
    return self.tienePermiso(permiso)
User.add_to_class('can_change_proyecto', can_change_proyecto)

def can_change_fase(self):
    permiso = 'change_fase'
    return self.tienePermiso(permiso)
User.add_to_class('can_change_fase', can_change_fase)

def can_change_group(self):
    permiso = 'change_group'
    return self.tienePermiso(permiso)
User.add_to_class('can_change_group', can_change_group)

def can_delete_user(self):
    permiso = 'delete_user'
    return self.tienePermiso(permiso)
User.add_to_class('can_delete_user', can_delete_user)

def can_delete_proyecto(self):
    permiso = 'delete_proyecto'
    return self.tienePermiso(permiso)
User.add_to_class('can_delete_proyecto', can_delete_proyecto)

def can_delete_fase(self):
    permiso = 'delete_fase'
    return self.tienePermiso(permiso)
User.add_to_class('can_delete_fase', can_delete_fase)

def can_delete_group(self):
    permiso = 'delete_group'
    return self.tienePermiso(permiso)
User.add_to_class('can_delete_group', can_delete_group)

###########################################Vistas de Control de Acceso #################################################

def can_administrar_fase(self):
    if self.is_active:
        if self.can_add_fase() or self.can_change_fase() or self.can_delete_fase():
            return True
    return False
User.add_to_class('can_administrar_fase', can_administrar_fase)

def can_administrar_proyecto(self):
    if self.is_active:
        return self.can_add_proyecto() or self.can_change_proyecto() or self.can_delete_proyecto() or self.can_administrar_fase()
    return False
User.add_to_class('can_administrar_proyecto', can_administrar_proyecto)

def can_administrar_usuario(self):
    if self.is_active:
        return self.can_add_user() or self.can_change_user() or self.can_delete_user()
    return False
User.add_to_class('can_administrar_usuario', can_administrar_usuario)

def can_administrar_rol(self):
    if self.is_active:
        return self.can_add_group() or self.can_change_group() or self.can_delete_group()
    return False
User.add_to_class('can_administrar_rol', can_administrar_rol)

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


usuario = User.objects.get(username="sgp")
usuario.groups.add(grupoAdministracion)
usuario.save()

    #Rol lider de Proyecto
grupoLiderProyecto, created = Group.objects.get_or_create(name='Lider de Proyecto')
if created:
    grupoLiderProyecto.save()
permisoAdd = Permission.objects.get(codename='add_fase')
permisoChange = Permission.objects.get(codename='change_fase')
permisoDelete = Permission.objects.get(codename='delete_fase')
grupoLiderProyecto.permissions.add(permisoAdd, permisoChange, permisoDelete)
