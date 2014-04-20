"""
Modelos del modulo de administracion
====================================
"""
from django.db import models
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType

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
Group.add_to_class('Usuario', models.ForeignKey(User, null=True))
Group.add_to_class('Fecha', models.DateTimeField(auto_now=True, null=True))


class Proyecto(models.Model):
    """
     * Contiene los campos de la tabla proyecto en la base de datos
      Variales
       Lider: es el usuario lider del proyecto
       Nombre: es el nombre que posee el proyecto
       Descripcion: es la decripcion del proyecto
       Fecha de inicio: es la fecha en que el proyecto dara inicio
       Fecha de finalizacion: es la fecha en la que el proyecto estara finalizado
       Usuario: usuario que creo el proyecto
       Fecha: es la fecha de creacion del proyecto
    """
    Lider = models.ForeignKey(User)
    Nombre = models.CharField(max_length=30, unique=True)
    Descripcion = models.TextField()
    Fecha_inicio = models.DateField('Fecha de inicio')
    Fecha_finalizacion = models.DateField('Fecha de finalizacion')
    #Usuario = models.ForeignKey(User)
    Fecha = models.DateTimeField(auto_now=True)


class Fase(models.Model):
    Nombre = models.CharField(max_length=50, unique=True)
    Descripcion = models.TextField()
    Usuario = models.ForeignKey(User)
    Proyecto = models.ForeignKey(Proyecto)
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
