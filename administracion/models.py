
from django.db import models
from django import forms
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin import widgets
import reversion

User.add_to_class('direccion', models.TextField(null=True, blank=True))
User.add_to_class('telefono', models.PositiveIntegerField(null=True, blank=True))
User.add_to_class('observacion', models.TextField(null=True, blank=True))
Group.add_to_class('Usuario', models.ForeignKey(User, null=True))
Group.add_to_class('Fecha', models.DateTimeField(auto_now=True, null=True))




def tienePermiso(self, permiso):
    for grupo in self.groups.all():
        for permisoUsuario in grupo.permissions.all():
            if permisoUsuario.codename == permiso:
                return True
    return False

User.add_to_class('tienePermiso', tienePermiso)

def accesoDesarrollo(self):
    permiso = 'acceso_desarrollo'
    return self.tienePermiso(permiso)

User.add_to_class('accesoDesarrollo', accesoDesarrollo)

def accesoLiderProyecto(self):
    rol='Lider de Proyecto'
    for grupo in self.groups.all():
        if grupo.name ==rol:
                return True
    return False

def accesoAdministrador(self):
    rol='Administracion'
    for grupo in self.groups.all():
        if grupo.name ==rol:
                return True
    return False
User.add_to_class('accesoLiderProyecto', accesoLiderProyecto)
User.add_to_class('accesoAdministrador', accesoAdministrador)

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

def can_add_atributo(self):
    permiso = 'add_atributo'
    return self.tienePermiso(permiso)
User.add_to_class('can_add_atributo', can_add_atributo)

def can_add_tipodeitem(self):
    permiso = 'add_tipodeitem'
    return self.tienePermiso(permiso)
User.add_to_class('can_add_tipodeitem', can_add_tipodeitem)

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

def can_change_atributo(self):
    permiso = 'change_atributo'
    return self.tienePermiso(permiso)
User.add_to_class('can_change_atributo', can_change_atributo)

def can_change_tipodeitem(self):
    permiso = 'change_tipodeitem'
    return self.tienePermiso(permiso)
User.add_to_class('can_change_tipodeitem', can_change_tipodeitem)

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

def can_delete_atributo(self):
    permiso = 'delete_atributo'
    return self.tienePermiso(permiso)
User.add_to_class('can_delete_atributo', can_delete_atributo)

def can_delete_tipodeitem(self):
    permiso = 'delete_tipodeitem'
    return self.tienePermiso(permiso)
User.add_to_class('can_delete_tipodeitem', can_delete_tipodeitem)

###########################################Vistas de Control de Acceso #################################################

def can_consultar_fase(self):
    permiso = 'consulta_fase'
    return self.tienePermiso(permiso)
User.add_to_class('can_consultar_fase', can_consultar_fase)

def can_consultar_proyecto(self):
    permiso = 'consulta_proyecto'
    return self.tienePermiso(permiso)
User.add_to_class('can_consultar_proyecto', can_consultar_proyecto)

def can_consultar_usuario(self):
    permiso = 'consulta_user'
    return self.tienePermiso(permiso)
User.add_to_class('can_consultar_usuario', can_consultar_usuario)

def can_consultar_rol(self):
    permiso = 'consulta_group'
    return self.tienePermiso(permiso)
User.add_to_class('can_consultar_rol', can_consultar_rol)

def can_consultar_atributo(self):
    permiso = 'consulta_atributo'
    return self.tienePermiso(permiso)
User.add_to_class('can_consultar_atributo', can_consultar_atributo)

def can_consultar_tipodeitem(self):
    permiso = 'consulta_tipodeitem'
    return self.tienePermiso(permiso)
User.add_to_class('can_consultar_tipodeitem', can_consultar_tipodeitem)


class Proyecto(models.Model):
    """
    Clase Proyecto:
        * Contiene los campos de la tabla proyecto en la base de datos

        * Variales
            -   Lider: es el usuario lider del proyecto
            -   Nombre: es el nombre que posee el proyecto
            -   Descripcion: es la decripcion del proyecto
            -   Fecha de inicio: es la fecha en que el proyecto dara inicio
            -   Fecha de finalizacion: es la fecha en la que el proyecto estara finalizado
            -   Fecha: es la fecha de creacion del proyecto
    """
    Lider = models.ForeignKey(User, related_name='Lider')
    Nombre = models.CharField(max_length=30, unique=True)
    Descripcion = models.TextField(max_length=100)
    Fecha_inicio = models.DateField('Fecha de inicio')
    Fecha_finalizacion = models.DateField('Fecha de finalizacion')
    Estado = models.CharField(max_length=2,
                              choices=( ('P', 'Pendiente'),
                                        ('A', 'Activo'),
                                        ('C', 'Cancelado'),
                                        ('F', 'Finalizado'),)
                              , default= 'P')
    Usuario = models.ForeignKey(User, related_name='Usuario_Creador')
    Usuarios = models.ManyToManyField(User, related_name='Participantes')
    Fecha = models.DateTimeField(auto_now=True)
    nFases = models.IntegerField(default=0)

    def __unicode__(self):
        return self.Nombre

class Fase(models.Model):
    """
    Clase Fase:
        * Contiene los campos de la tabla fase en la base de datos

        * Variales
            -   Nombre: es el nombre que posee la fase
            -   Descripcion: es la decripcion de la fase
            -   Usuario: usuario que creo la fase
            -   Proyecto: proyecto al que corresponde la fase
            -   Fecha: es la fecha de creacion de la fase
    """
    Nombre = models.CharField(max_length=50)
    Descripcion = models.TextField(max_length=100)
    Usuario = models.ForeignKey(User)
    Proyecto = models.ForeignKey(Proyecto)
    Fecha = models.DateTimeField(auto_now=True)
    Numero = models.PositiveIntegerField()
    Usuarios = models.ManyToManyField(User, related_name='Participantes_Fase')

    def __unicode__(self):
        return self.Nombre


    def ordenar_fase_subir(self):
        try:
            faseTemporal = Fase.objects.filter(Proyecto=self.Proyecto.pk).filter(Numero__lt=self.Numero).order_by('-Numero').first()
            numeroTemporal = faseTemporal.Numero
            faseTemporal.Numero = self.Numero
            faseTemporal.save()
            self.Numero = numeroTemporal
            self.save()
        finally:
            return

    def ordenar_fase_bajar(self):
        try:
            faseTemporal = Fase.objects.filter(Proyecto=self.Proyecto).filter(Numero__gt=self.Numero).first()
            numeroTemporal = faseTemporal.Numero
            faseTemporal.Numero = self.Numero
            faseTemporal.save()
            self.Numero = numeroTemporal
            self.save()
        finally:
            return


    class Meta:
        ordering = ["Numero"]
        unique_together = ("Nombre", "Proyecto")

class Atributo(models.Model):

    """

    """
    Nombre = models.CharField(max_length=30, unique=True)
    NUMERICO = 'N'
    CADENA = 'C'
    FECHA = 'F'
    HORA = 'H'
    LOGICO = 'L'
    TEXTO = 'T'
    TIPO_CHOICES = (
        (NUMERICO, 'Numerico'),
        (CADENA, 'Cadena'),
        (FECHA, 'Fecha'),
        (HORA, 'Hora'),
        (LOGICO, 'Logico'),
    )
    Tipo = models.CharField(max_length=1, choices=(TIPO_CHOICES))
    Descripcion = models.TextField(max_length=100, blank=True)
    Usuario = models.ForeignKey(User)
    Fase = models.ForeignKey(Fase)
    Fecha = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.Nombre

class TipoDeItem(models.Model):
    Nombre = models.CharField(max_length=30)
    Usuario = models.ForeignKey(User)
    Fecha = models.DateTimeField(auto_now=True)
    Atributos = models.ManyToManyField(Atributo)
    Fase = models.ForeignKey(Fase)

    def __unicode__(self):
        return self.Nombre



