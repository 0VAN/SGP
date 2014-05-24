
from django.db import models
from django.contrib.auth.models import User, Group, Permission
from django.utils import six

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

def esDesarrollador(self):
    rol='Desarrollador'
    for grupo in self.groups.all():
        if grupo.name ==rol:
                return True
    return False

User.add_to_class('esDesarrollador', esDesarrollador)

def esLider(self):
    rol='Lider de Proyecto'
    for grupo in self.groups.all():
        if grupo.name ==rol:
                return True
    return False
User.add_to_class('esLider', esLider)

def esAdministrador(self):
    rol='Administrador'
    for grupo in self.groups.all():
        if grupo.name ==rol:
                return True
    return False
User.add_to_class('esAdministrador', esAdministrador)

def integraComite(self):
    rol='Integrante de Comite'
    for grupo in self.groups.all():
        if grupo.name ==rol:
                return True
    return False
User.add_to_class('integraComite', integraComite)

########################################################################################################################
#########################PERMISOS SOBRE USUARIOS########################################################################
########################################################################################################################
def puede_agregar_usuarios(self):
    permiso = 'add_user'
    return self.tienePermiso(permiso)
User.add_to_class('puede_agregar_usuarios', puede_agregar_usuarios)
def puede_modificar_usuarios(self):
    permiso = 'change_user'
    return self.tienePermiso(permiso)
User.add_to_class('puede_modificar_usuarios', puede_modificar_usuarios)
def puede_eliminar_usuarios(self):
    permiso = 'delete_user'
    return self.tienePermiso(permiso)
User.add_to_class('puede_eliminar_usuarios', puede_eliminar_usuarios)
def puede_consultar_usuarios(self):
    permiso = 'consulta_user'
    return self.tienePermiso(permiso)
User.add_to_class('puede_consultar_usuarios', puede_consultar_usuarios)
########################################################################################################################
#############PERMISOS SOBRE PROYECTOS###################################################################################
########################################################################################################################
def puede_agregar_proyectos(self):
    permiso = 'add_proyecto'
    return self.tienePermiso(permiso)
User.add_to_class('puede_agregar_proyectos', puede_agregar_proyectos)
def puede_modificar_proyectos(self):
    permiso = 'change_proyecto'
    return self.tienePermiso(permiso)
User.add_to_class('puede_modificar_proyectos', puede_modificar_proyectos)
def puede_eliminar_proyectos(self):
    permiso = 'delete_proyecto'
    return self.tienePermiso(permiso)
User.add_to_class('puede_eliminar_proyectos', puede_eliminar_proyectos)
def puede_consultar_proyectos(self):
    permiso = 'consulta_proyecto'
    return self.tienePermiso(permiso)
User.add_to_class('puede_consultar_proyectos', puede_consultar_proyectos)
########################################################################################################################
#################################PERMISOS SOBRE FASES###################################################################
########################################################################################################################
def puede_agregar_fases(self):
    permiso = 'add_fase'
    return self.tienePermiso(permiso)
User.add_to_class('puede_agregar_fases', puede_agregar_fases)
def puede_modificar_fases(self):
    permiso = 'change_fase'
    return self.tienePermiso(permiso)
User.add_to_class('puede_modificar_fases', puede_modificar_fases)
def puede_eliminar_fases(self):
    permiso = 'delete_fase'
    return self.tienePermiso(permiso)
User.add_to_class('puede_eliminar_fases', puede_eliminar_fases)
def puede_consultar_fases(self):
    permiso = 'consulta_fase'
    return self.tienePermiso(permiso)
User.add_to_class('puede_consultar_fases', puede_consultar_fases)
########################################################################################################################
##################################PERMISOS SOBRE ROLES##################################################################
########################################################################################################################
def puede_agregar_roles(self):
    permiso = 'add_group'
    return self.tienePermiso(permiso)
User.add_to_class('puede_agregar_roles', puede_agregar_roles)
def puede_modificar_roles(self):
    permiso = 'change_group'
    return self.tienePermiso(permiso)
User.add_to_class('puede_modificar_roles', puede_modificar_roles)
def puede_eliminar_roles(self):
    permiso = 'delete_group'
    return self.tienePermiso(permiso)
User.add_to_class('puede_eliminar_roles', puede_eliminar_roles)
def puede_consultar_roles(self):
    permiso = 'consulta_group'
    return self.tienePermiso(permiso)
User.add_to_class('puede_consultar_roles', puede_consultar_roles)
########################################################################################################################
###################################PERMISOS SOBRE ATRIBUTOS#############################################################
########################################################################################################################
def puede_agregar_atributos(self):
    permiso = 'add_atributo'
    return self.tienePermiso(permiso)
User.add_to_class('puede_agregar_atributos', puede_agregar_atributos)
def puede_modificar_atributos(self):
    permiso = 'change_atributo'
    return self.tienePermiso(permiso)
User.add_to_class('puede_modificar_atributos', puede_modificar_atributos)
def puede_eliminar_atributos(self):
    permiso = 'delete_atributo'
    return self.tienePermiso(permiso)
User.add_to_class('puede_eliminar_atributos', puede_eliminar_atributos)
def puede_consultar_atributos(self):
    permiso = 'consulta_atributo'
    return self.tienePermiso(permiso)
User.add_to_class('puede_consultar_atributos', puede_consultar_atributos)
########################################################################################################################
#####################################PERMISOS SOBRE TIPOS DE ITEMS#######################################################
########################################################################################################################
def puede_agregar_tipodeitem(self):
    permiso = 'add_tipodeitem'
    return self.tienePermiso(permiso)
User.add_to_class('puede_agregar_tipodeitem', puede_agregar_tipodeitem)
def puede_modificar_tipodeitem(self):
    permiso = 'change_tipodeitem'
    return self.tienePermiso(permiso)
User.add_to_class('puede_modificar_tipodeitem', puede_modificar_tipodeitem)
def puede_eliminar_tipodeitem(self):
    permiso = 'delete_tipodeitem'
    return self.tienePermiso(permiso)
User.add_to_class('puede_eliminar_tipodeitem', puede_eliminar_tipodeitem)
def puede_consultar_tipodeitem(self):
    permiso = 'consulta_tipodeitem'
    return self.tienePermiso(permiso)
User.add_to_class('puede_consultar_tipodeitem', puede_consultar_tipodeitem)


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

    def __str__(self):
        return "%s | %s | %s" % (
            six.text_type(self.Nombre),
            six.text_type(self.Fase.Nombre),
            six.text_type(self.Fase.Proyecto.Nombre))

