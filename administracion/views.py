# -*- encoding: utf-8 -*-
from django.contrib.auth import models
from django.shortcuts import render_to_response, render, HttpResponseRedirect, HttpResponse, RequestContext, get_object_or_404
from administracion.forms import ProyectoForm, UsuarioModForm, UsuarioDelForm, FaseForm, RolForm, AsignarRol, AtributoForm, tipoItemForm
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group , timezone
from administracion.models import Proyecto, Fase, Atributo, TipoDeItem
from django.contrib.auth.models import User, Group, Permission
from administracion.models import Proyecto, Fase
from django.core.exceptions import *


# Create your views here.
########################################################################################################################
#############################Vistas de iniciar sesion, cerrar sesion, administracion####################################
########################################################################################################################

@login_required(login_url='/iniciar_sesion')
def administracion(request):
    """

    :param request:
    :return:

    Vista que muestra el contenido privado del modulo de administracion

    | Recibe como parametro un request y retorna la pagina web admiistracion.html donde se muestra la
    | lista de usuarios del sistema si el usuario_actor posee los permisos correspondientes

    * Variables
        -   lista_usuarios: es la lista de usuarios existentes en el sistema
        -   usuario_actor: es el usuario que realiza la accion
    """
    lista_usuarios = User.objects.all()
    usuario_actor = request.user
    seleccionado = 0
    return render_to_response('administracion.html', {'lista_usuarios': lista_usuarios, 'usuario_actor':usuario_actor,'seleccionado':seleccionado},
                              context_instance=RequestContext(request))
########################################################################################################################
#############################################Vistas de Administracion de Usuarios#######################################
########################################################################################################################
@login_required( login_url="/iniciar_sesion")
def administrar_usuario(request):
    """

    :param request:
    :return:

    Vista de administrar usuario

    | Recibe como parametro un request y retorna la pagina web administrar_usuario.html donde se muestra
    | la lista de usuarios si el usuario_actor posee los permsos correspondientes

    * Variables
        -   usuario_actor: es el usuario que realiza la accion
        -   lista_usuarios: es la lista de usuarios existentes en el sistema
    """
    usuario_actor = request.user
    lista_usuarios = User.objects.all()
    return render_to_response('usuario/administrar_usuario.html', {'usuario_actor':usuario_actor,'lista_usuarios':lista_usuarios},
                              context_instance=RequestContext(request))
@user_passes_test( User.can_add_user , login_url="/iniciar_sesion")
def crear_usuario(request):
    """

    :param request:
    :return:

    Vista de creacion de nuevo usuario

    | Recibe como parametro un request y retorna la pagina web form_usuario.html donde se debe completar
    | los datos del usuario y luego operacion_usuario_exito.html si se completo debidamente el formulario

    * Variables
        -   usuario_actor: es el usuario que realiza la accion
        -   formulario: es el fomrulario que debe completar el usuario_actor
        -   lista_usuarios: es la lista de usuarios existentes en el sistema
    """
    usuario_actor = request.user
    if request.method == 'POST':
        formulario = UserCreationForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            lista_usuarios = User.objects.all()
            return render_to_response('usuario/operacion_usuario_exito.html',
                                      {'mensaje': 'El nuevo usuario fue creado exitosamente', 'usuario_actor': usuario_actor,
                                       'lista_usuarios': lista_usuarios}, context_instance=RequestContext(request))
    else:
        formulario = UserCreationForm()
    return render_to_response('usuario/form_usuario.html',
                              {'formulario': formulario, 'operacion': 'Ingrese los datos del nuevo usuario',
                               'usuario_actor': usuario_actor}, context_instance=RequestContext(request))

@login_required(login_url="/iniciar_sesion")
def modificar_usuario(request, id_usuario_p):
    """

    :param request:
    :return:

    Vista de modificacion de nuevo usuario

    | Recibe como parametro un request y retorna la pagina web form_usuario.html donde se debe completar
    | los datos el usuario y luego operacion_usuario_exito.html si se completo debidamente el formulario

    * Variables
        -   usuario_actor: es el usuario que realiza la accion
        -   formulario: es el fomrulario que debe completar el usuario_actor
        -   lista_usuarios: es la lista de usuarios existentes en el sistema
    """
    usuario_parametro = User.objects.get(pk=id_usuario_p)
    lista_usuarios = User.objects.all()
    if request.method == 'POST':
        formulario = UsuarioModForm(request.POST, instance=usuario_parametro)
        if formulario.is_valid():
           formulario.save()
           return render_to_response('usuario/operacion_usuario_exito.html',
                                     {'mensaje': 'Se ha actualizado la informacion personal',
                                       'usuario_actor': request.user, 'usuario_parametro': usuario_parametro,
                                      'lista_usuarios': lista_usuarios}, context_instance=RequestContext(request))
    else:
        formulario = UsuarioModForm(instance=usuario_parametro)
    return render(request, 'usuario/form_usuario_mod.html',
                  {'usuario_actor': request.user, 'formulario': formulario, 'operacion': 'Modificar usuario',
                   'usuario_parametro': usuario_parametro},
                  context_instance=RequestContext(request))

@login_required(login_url="/iniciar_sesion")
def pass_change(request, id_usuario_p):
    usuario_parametro = User.objects.get(pk=id_usuario_p)
    lista_usuarios = User.objects.all()
    if request.method == 'POST':
        formulario = SetPasswordForm(data=request.POST, user= usuario_parametro)
        if formulario.is_valid():
           formulario.save()
           return render_to_response('usuario/operacion_usuario_exito.html',
                                     {'mensaje': 'Se ha actualizado la contraseña',
                                       'usuario_actor': request.user, 'usuario_parametro': usuario_parametro,
                                      'lista_usuarios': lista_usuarios}, context_instance=RequestContext(request))
    else:
        formulario = SetPasswordForm(user=usuario_parametro)
    return render(request, 'usuario/form_usuario.html',
                  {'usuario_actor': request.user, 'formulario': formulario, 'operacion': 'Cambio de contraseña',
                   'usuario_parametro': usuario_parametro},
                  context_instance=RequestContext(request))

@user_passes_test( User.can_consultar_usuario , login_url="/iniciar_sesion")
def detalle_usuario(request, id_usuario_p):
    """

    :param request:
    :param id_usuario_p:
    :return:

    Vista detalle del usuario

    Recibe un request y un id de usuario como parametro y retorna la pagina web detalle_usuario.html

    * Variables
        -   usuario_parametro: es el usuario que se vera en detalle en la pagina web detalle_usuario.html
    """
    usuario_parametro = User.objects.get(pk=id_usuario_p)
    return render_to_response('usuario/detalle_usuario.html', {'usuario_actor': request.user,
                              'usuario_parametro': usuario_parametro}, context_instance=RequestContext(request))


@user_passes_test( User.can_change_user , login_url="/iniciar_sesion")
def cambioEstado_usuario_form(request, id_usuario_p):
    """

    :param request:
    :param id_usuario_p:
    :return:

    Vista de cambio de estado de usuario

    | Recibe un request y un id de usuario y retorna la pagina web form_usuario.html donde se debe
    | completar los datos del usuario y luego operacion_usuario_exito.html si se completo debidamente
    | el formulario

    * Variables
        -   usuario_parametro: es el usuario cuyo estado podra se cambiado en la pagina web form_usuario.html
        -   usuario_actor: es el usuario que realiza la accion
        -   lista_usuarios: es la lista de usuarios existentes en el sistema
    """
    usuario_parametro = User.objects.get(pk=id_usuario_p)
    usuario_actor = request.user
    lista_usuarios = User.objects.all()
    if request.method == 'POST':
        formulario = UsuarioDelForm(request.POST, instance=usuario_parametro)
        if formulario.is_valid():
           formulario.save()
           return render_to_response('usuario/operacion_usuario_exito.html',
                                     {'mensaje': 'Cambio de estado de usuario con exito', 'usuario_actor':usuario_actor,
                                      'lista_usuarios': lista_usuarios}, context_instance=RequestContext(request))
    else:
        formulario = UsuarioDelForm(instance=usuario_parametro)
    return render_to_response('usuario/form_usuario.html',
                   {'usuario_actor': usuario_actor, 'usuario_parametro': usuario_parametro,
                    'formulario': formulario, 'operacion': 'Cambio de estado del usuario'},
                   context_instance=RequestContext(request))

########################################################################################################################
###########################################Vistas de Administrar Proyecto###############################################
########################################################################################################################
@login_required(login_url="/iniciar_sesion")
def administrar_proyecto(request):
    """

    :param request:
    :return:

    Vista administrar proyecto

    Recibe como parametro un request y retorna la pagina web administrar_proyecto.html

    * Varaibles
        -   lista_proyectos: es la lista de proyectos existentes en el sistema
        -   usuario_actor: es el usuario que realiza la accion
    """
    lista_proyectos = Proyecto.objects.all()
    usuario_actor = request.user
    return render_to_response('proyecto/administrar_proyecto.html',
                              {'lista_proyectos': lista_proyectos, 'usuario_actor': usuario_actor}, context_instance=RequestContext(request))

@user_passes_test( User.can_add_proyecto , login_url="/iniciar_sesion")
def nuevo_proyecto(request):
    """

    :param request:
    :return:

    Vista nuevo proyecto

    | Recibe como parametro un request y retorna la pagina web crear_proyecto.html donde se debe
    | completar los datos del proyecto y luego proyecto_exito.html si se completo debidamente
    | el formulario

    * Variables
        -   usuario_actor: es el usuario que realiza la accion
        -   lista_proyectos: es la lista de todos los proyectos existentes en el sistema
        -   formulario: es el formulario que el usuario debe completar
    """
    usuario_actor = request.user
    proyecto = Proyecto(Usuario=usuario_actor)
    if request.method == 'POST':
        lista_proyectos = Proyecto.objects.all()
        formulario = ProyectoForm(request.POST, instance=proyecto)
        if formulario.is_valid():
            formulario.save()

            return render_to_response('proyecto/proyecto_exito.html',
                                      {'mensaje': 'El nuevo proyecto ha sido creado exitosamente',
                                       'usuario_actor': usuario_actor, 'lista_proyectos': lista_proyectos},
                                      context_instance=RequestContext(request))
    else:
        formulario = ProyectoForm(instance=proyecto)
    return render_to_response('proyecto/crear_proyecto.html',
                              {'formulario': formulario, 'operacion':'Ingrese los datos del proyecto'
                               , 'usuario_actor': usuario_actor}, context_instance=RequestContext(request))

@user_passes_test( User.can_consultar_proyecto , login_url="/iniciar_sesion")
def detalle_proyecto(request, id_proyecto):
    """

    :param request:
    :param id_proyecto:
    :return:

    Vista detalle de proyecto

    | Recibe un request y un id de proyecto y retorna una pagina web detalle_proyecto.html con los detalles
    | de un proyecto

    * Variables
        -   usuario_actor: es el usuario que realiza la accion
        -   proyecto: es el proyecto que sera visualizado en detalle
    """
    usuario_actor = request.user
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    return render_to_response('proyecto/detalle_proyecto.html', {'usuario_actor': usuario_actor, 'proyecto': proyecto},
                              context_instance=RequestContext(request))

@login_required(login_url="/iniciar_sesion")
def iniciar_proyecto(request, id_proyecto):
    """

    :param request:
    :param id_proyecto:
    :return:
    """
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    proyecto.Estado = 'A'
    proyecto.Fecha_inicio = timezone.now()
    proyecto.save()
    return render_to_response('proyecto/proyecto_exito.html', {'usuario_actor':request.user, 'proyecto':proyecto,
                              'mensaje': 'Se ha dado inicio al proyecto', 'lista_proyectos':Proyecto.objects.all()}
                              ,context_instance=RequestContext(request))

def confirmar_iniciar_proyecto(request, id_proyecto):
    """

    :param request:
    :param id_proyecto:
    :return:
    """
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    if proyecto.Estado == 'A':
        return render_to_response('proyecto/proyecto_error.html', {'usuario_actor':request.user, 'proyecto':proyecto,
                              'mensaje': 'No puedes iniciar un proyecto que ya ha sido iniciado, ver detalles', 'lista_proyectos':Proyecto.objects.all()}
                              ,context_instance=RequestContext(request))
    else:
        if proyecto.Estado == 'C':
            return render_to_response('proyecto/proyecto_error.html', {'usuario_actor':request.user, 'proyecto':proyecto,
                              'mensaje': 'No puedes iniciar un proyecto que ya ha sido cancelado, ver detalles', 'lista_proyectos':Proyecto.objects.all()}
                              ,context_instance=RequestContext(request))
        else:
            if proyecto.Estado == 'F':
                return render_to_response('proyecto/proyecto_error.html', {'usuario_actor':request.user, 'proyecto':proyecto,
                              'mensaje': 'No puedes iniciar un proyecto que ya ha finalizado, ver detalles', 'lista_proyectos':Proyecto.objects.all()}
                              ,context_instance=RequestContext(request))
            else:
                return render_to_response('proyecto/conf_iniciar_proyecto.html', {'usuario_actor': request.user, 'proyecto': proyecto
                                , 'lista_proyectos': Proyecto.objects.all()}, context_instance=RequestContext(request))

def eliminar_proyecto(request, id_proyecto):
    """

    :param request:
    :param id_proyecto:
    :return:
    """
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    proyecto.Estado = 'C'
    proyecto.Fecha_finalizacion = timezone.now()
    proyecto.save()
    return render_to_response('proyecto/proyecto_exito.html', {'usuario_actor':request.user, 'proyecto':proyecto,
                              'mensaje': 'Se ha cancelado el proyecto seleccionado ', 'lista_proyectos': Proyecto.objects.all()}
                              ,context_instance=RequestContext(request))
def confirmar_eliminar_proyecto(request, id_proyecto):
    """

    :param request:
    :param id_proyecto:
    :return:
    """
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    if proyecto.Estado == 'C':
        return render_to_response('proyecto/proyecto_error.html', {'usuario_actor':request.user, 'proyecto':proyecto,
                              'mensaje': 'No puedes cancelar un proyecto que ya ha sido cancelado, ver detalles', 'lista_proyectos': Proyecto.objects.all()}
                              ,context_instance=RequestContext(request))
    else:
        return render_to_response('proyecto/conf_eliminar_proyecto.html', {'usuario_actor': request.user, 'proyecto': proyecto
                                , 'lista_proyectos': Proyecto.objects.all()}, context_instance=RequestContext(request))


def modificar_proyecto(request, id_proyecto):
    """

    :param request:
    :param id_proyecto:
    :return:
    """
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    if proyecto.Estado == 'P':
        if request.method == 'POST':
            formulario = ProyectoForm(request.POST, instance=proyecto)
            if formulario.is_valid():
                formulario.save()
                return render_to_response('proyecto/proyecto_exito.html',
                                      {'mensaje': 'El proyecto ha sido modificado exitosamente',
                                       'usuario_actor': request.user, 'lista_proyectos': Proyecto.objects.all()},
                                      context_instance=RequestContext(request))
        else:
            formulario = ProyectoForm(instance=proyecto)
            return render_to_response('proyecto/crear_proyecto.html',
                              {'formulario': formulario, 'operacion':'Ingrese los datos del proyecto'
                               , 'usuario_actor': request.user}, context_instance=RequestContext(request))
    else:
        if proyecto.Estado == 'C':
            return render_to_response('proyecto/proyecto_error.html',
                                      {'mensaje': 'No puedes modificar los datos de un proyecto que ya ha sido cancelado, ver detalles',
                                       'usuario_actor': request.user, 'lista_proyectos': Proyecto.objects.all()},
                                      context_instance=RequestContext(request))
        else:
            if proyecto.Estado == 'A':
                return render_to_response('proyecto/proyecto_error.html',
                                      {'mensaje': 'No puedes modificar los datos de un proyecto que ya ha iniciado, ver detalles',
                                       'usuario_actor': request.user, 'lista_proyectos': Proyecto.objects.all()},
                                      context_instance=RequestContext(request))
            else:
                if proyecto.Estado == 'F':
                    return render_to_response('proyecto/proyecto_error.html',
                                      {'mensaje': 'No puedes modificar los datos de un proyecto que ya ha finalizado, ver detalles',
                                       'usuario_actor': request.user, 'lista_proyectos': Proyecto.objects.all()},
                                      context_instance=RequestContext(request))

########################################################################################################################
###########################################Vistas de administracion de Fase#############################################
########################################################################################################################

@user_passes_test(User.can_consultar_fase, login_url="/iniciar_sesion")
def administrar_fases(request, id_proyecto):
    """

    :param request:
    :param id_proyecto:
    :return:

    Vista administrar fase

    Recibe un request y un id de proyecto y retorna la pagina web adm-fases.html

    * Variables
        -   usuario_actor: usuario que realiza la accion
        -   proyecto: es el proyecto cuyas fases se desea administrar
        -   fases: indica que la fase correpondera a un proyecto especifico
    """
    usuario_actor = request.user
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    lista_fases = Fase.objects.filter(Proyecto=id_proyecto)
    return render_to_response('proyecto/fase/adm-fases.html',
                              {'usuario_actor': usuario_actor, 'lista_fases': lista_fases, 'proyecto': proyecto}
                              , context_instance=RequestContext(request))


def ordenar_fase_subir(request, id_fase):
    fase = Fase.objects.get(pk=id_fase)
    fase.ordenar_fase_subir()
    return administrar_fases(request,fase.Proyecto.id)

def ordenar_fase_bajar(request, id_fase):
    fase = Fase.objects.get(pk=id_fase)
    fase.ordenar_fase_bajar()
    return administrar_fases(request,fase.Proyecto.id)


@user_passes_test(User.can_add_fase, login_url="/iniciar_sesion")
def crear_fase(request, id_proyecto):
    """
    :param request:
    :param id_proyecto:
    :return: fase_form.html

    Vista crear fase

    Recibe como parametros un request y un id de proyecto y retorna la pagina web fase_form.html

    * Variables
        -   usuario_actor: usuario que realiza la accion
        -   proyecto: es el proyecto cuyas fases se desea administrar
        -   fases: indica que la fase correpondera a un proyecto especifico
    """
    usuario_actor = request.user
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    fase = Fase(Usuario= usuario_actor, Proyecto=proyecto)
    fase.Numero = 0
    lista_fases = Fase.objects.filter(Proyecto=proyecto)
    if request.method=='POST':
        formulario = FaseForm(request.POST, instance=fase)
        if formulario.is_valid():
            proyecto.nFases+=1
            proyecto.save()
            fase.Numero = proyecto.nFases
            formulario = FaseForm(request.POST, instance=fase)
            formulario.save()
            return render_to_response(
                'proyecto/fase/fases_exito.html',
                {'usuario_actor': usuario_actor, 'proyecto': proyecto, 'lista_fases': lista_fases, 'mensaje': 'Se ha creado la fase exitosamente'},
                context_instance=RequestContext(request)
            )
    else:
        formulario = FaseForm(instance=fase)
    return render_to_response('proyecto/fase/fase_form.html',
                              {'usuario_actor': usuario_actor, 'formulario': formulario, 'proyecto': proyecto,
                               'operacion':'Ingrese los datos de la fase'},
                              context_instance=RequestContext(request))


@user_passes_test(User.can_consultar_fase, login_url="/iniciar_sesion")
def detalle_fase(request, idFase, id_proyecto):
    """

    :param request:
    :param idFase:
    :param id_proyecto:
    :return:

    Vista detalle fase

    | Recibe como parametros un request, un id de fase y un id de proyecto, y retorna la pagina web
    | detallefase.html que muestra en detalle la informacion de dicha fase

    * Variables
        -   usuario_actor: usuario que realiza la accion
        -   proyecto: es el proyecto cuyas fases se desea administrar
        -   fases: indica que la fase correpondera a un proyecto especifico
    """
    usuario_actor = request.user
    fase = Fase.objects.get(pk=idFase)
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    return render_to_response('proyecto/fase/detallefase.html',
                              {'usuario_actor': usuario_actor, 'fase': fase, 'proyecto':proyecto},
                              context_instance=RequestContext(request))

@login_required(login_url="/iniciar_sesion")
def modificar_fase(request, idFase, id_proyecto):
    """

    :param request:
    :param idFase:
    :param id_proyecto:
    :return:
    """
    usuario_actor = request.user
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    lista_fases = Fase.objects.filter(Proyecto=id_proyecto)

    if proyecto.Estado == 'A':
                return render_to_response('proyecto/fase/fases_error.html',
                              {'usuario_actor': usuario_actor, 'proyecto': proyecto, 'lista_fases': lista_fases,
                               'mensaje': 'No puedes modificar los datos de una fase de un proyecto que ha iniciado'},
                              context_instance=RequestContext(request))
    else:
        if proyecto.Estado == 'C':
                return render_to_response('proyecto/fase/fases_error.html',
                              {'usuario_actor': usuario_actor, 'proyecto': proyecto, 'lista_fases': lista_fases,
                               'mensaje': 'No puedes modificar los datos de una fase de un proyecto que ha sido cancelado'},
                              context_instance=RequestContext(request))
        else:
            if proyecto.Estado == 'F':
                return render_to_response('proyecto/fase/fases_error.html',
                              {'usuario_actor': usuario_actor, 'proyecto': proyecto, 'lista_fases': lista_fases,
                               'mensaje': 'No puedes modificar los datos de una fase de un proyecto que ha finalizado'},
                              context_instance=RequestContext(request))
            else:
                fase = Fase.objects.get(pk=idFase)
                formulario = FaseForm(request.POST, instance=fase)
                if formulario.is_valid():
                    formulario.save()
                    return render_to_response('proyecto/fase/fases_exito.html',
                              {'usuario_actor': usuario_actor, 'proyecto': proyecto, 'lista_fases': lista_fases,
                               'mensaje': 'Se ha modificado la fase exitosamente'},
                              context_instance=RequestContext(request))
                else:
                    formulario = FaseForm(instance=fase)
                    return render_to_response('proyecto/fase/fase_form.html',
                              {'usuario_actor': usuario_actor, 'formulario': formulario, 'proyecto': proyecto,
                               'fase': fase, 'operacion': 'Modificar Fase'}, context_instance=RequestContext(request))

@login_required(login_url="/iniciar_sesion")
def confirmar_eliminar_fase(request, idFase, id_proyecto):
    """

    :param request:
    :param idFase:
    :param id_proyecto:
    :return:
    """
    usuario_actor = request.user
    proyecto = Proyecto.objects.get(pk=id_proyecto)

    lista_fases = Fase.objects.filter(Proyecto=id_proyecto)
    if proyecto.Estado == 'A':

        return render_to_response('proyecto/fase/fases_error.html',
                      {'usuario_actor': usuario_actor, 'proyecto': proyecto, 'lista_fases': lista_fases,
                       'mensaje': 'No puedes eliminar una fase de un proyecto que ha iniciado'},
                      context_instance=RequestContext(request))
    elif proyecto.Estado == 'C':
        return render_to_response('proyecto/fase/fases_error.html',
                      {'usuario_actor': usuario_actor, 'proyecto': proyecto, 'lista_fases': lista_fases,
                       'mensaje': 'No puedes eliminar una fase de un proyecto que ha sido cancelado'},
                      context_instance=RequestContext(request))
    elif proyecto.Estado == 'F':
        return render_to_response('proyecto/fase/fases_error.html',
                      {'usuario_actor': usuario_actor, 'proyecto': proyecto, 'lista_fases': lista_fases,
                       'mensaje': 'No puedes eliminar una fase de un proyecto que ha finalizado'},
                      context_instance=RequestContext(request))
    else:
        fase = Fase.objects.get(pk=idFase)
        return render_to_response('proyecto/fase/conf_eliminar_fase.html',
                      {'usuario_actor': usuario_actor, 'fase': fase, 'proyecto': proyecto},
                      context_instance=RequestContext(request))

@login_required(login_url="/iniciar_sesion")
def eliminar_fase(request, idFase, id_proyecto):
    """

    :param request:
    :param idFase:
    :param id_proyecto:
    :return:
    """
    fase = Fase.objects.get(pk=idFase)
    usuario_actor = request.user
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    proyecto.nFases-=1
    proyecto.save()
    reordenar(proyecto.id, fase.Numero)
    fase.delete()

    lista_fases = Fase.objects.filter(pk=id_proyecto)
    return render_to_response('proyecto/fase/fases_exito.html',
                              {'usuario_actor': usuario_actor, 'proyecto': proyecto, 'lista_fases': lista_fases,
                               'mensaje': 'Se ha eliminado la fase seleccionada'},
                              context_instance=RequestContext(request))
def reordenar(idproyecto, numero):
    proyecto = Proyecto.objects.get(pk=idproyecto)
    for n in range(numero+1, proyecto.nFases+2, 1):
        fase = Fase.objects.get(Proyecto=proyecto, Numero=n)
        fase.Numero-=1
        fase.save()
    return True




########################################################################################################################
###########################################Vistas de administracion de Rol##############################################
########################################################################################################################
@user_passes_test(User.can_consultar_rol, login_url="/iniciar_sesion")
def administrar_roles(request):
    """

    :param request:
    :return:
    """
    usuario_actor = request.user
    roles = Group.objects.all()
    return render_to_response('rol/administrar_rol.html',
                              {'usuario_actor': usuario_actor, 'roles': roles}, context_instance=RequestContext(request))

@user_passes_test(User.can_add_group, login_url="/iniciar_sesion")
def crear_rol(request):
    """

    :param request:
    :return:
    """
    mensaje="Rol creado con exito"
    usuario_actor = request.user
    rol = Group(Usuario=usuario_actor)
    roles = Group.objects.all()
    if request.method == 'POST':
        formulario = RolForm(request.POST, instance=rol)
        if formulario.is_valid():
            formulario.save()
            return render_to_response('rol/rol_exito.html',
                                      {'mensaje': mensaje, 'usuario_actor': usuario_actor, 'roles': roles},
                                      context_instance=RequestContext(request))
    else:
        formulario = RolForm(instance=rol)
    return render_to_response('rol/crear_rol.html',
                              {'formulario': formulario, 'operacion': 'Ingrese los datos del rol a crear',
                               'usuario_actor': usuario_actor},
                              context_instance=RequestContext(request))

@user_passes_test(User.can_consultar_rol, login_url="/iniciar_sesion")
def detalle_rol(request, idRol):
    """

    :param request:
    :param idRol:
    :return:
    """
    usuario_actor = request.user
    rol = Group.objects.get(pk=idRol)
    lista_permisos = rol.permissions.all()
    return render_to_response('rol/detallerol.html', {'usuario_actor': usuario_actor, 'rol': rol,'lista_permisos':lista_permisos},
                              context_instance=RequestContext(request))

@user_passes_test(User.can_change_group, login_url="/iniciar_sesion")
def modificar_rol(request, idRol):
    """

    :param request:
    :param idRol:
    :return:
    """
    usuario_actor = request.user
    rol = Group.objects.get(pk=idRol)
    roles = Group.objects.all()
    formulario = RolForm(request.POST, instance=rol)
    if formulario.is_valid():
        formulario.save()
        mensaje = 'El rol ha sido modificado exitosamente'
        return render_to_response('rol/rol_exito.html',
                                      {'mensaje': mensaje, 'usuario_actor': usuario_actor, 'roles': roles},
                                      context_instance=RequestContext(request))
    else:
        formulario = RolForm(instance=rol)
    return render_to_response('rol/modificar_rol.html',
                              {'usuario_actor': usuario_actor, 'rol':rol, 'formulario':formulario},
                              context_instance=RequestContext(request))

@user_passes_test(User.can_delete_group, login_url="/iniciar_sesion")
def confirmar_eliminar_rol(request, idRol):
    """

    :param request:
    :param idRol:
    :return:
    """
    usuario_actor = request.user
    rol = Group.objects.get(pk=idRol)
    return render_to_response('rol/conf_eliminar_rol.html', {'usuario_actor': usuario_actor, 'rol': rol},
                              context_instance=RequestContext(request))

@user_passes_test(User.can_delete_group, login_url="/iniciar_sesion")
def eliminar_rol(request, idRol):
    """

    :param request:
    :param idRol:
    :return:
    """
    rol = Group.objects.get(pk=idRol)
    rol.delete()
    usuario_actor = request.user
    roles = Group.objects.all()
    return render_to_response('rol/roleliminado.html',
                              {'usuario_actor': usuario_actor, 'roles': roles},
                              context_instance=RequestContext(request))

@user_passes_test(User.can_change_user, login_url="/iniciar_sesion")
def vista_asignar_rol(request):
    """

    :param request:
    :return:
    """
    usuario_actor = request.user
    lista_usuarios = User.objects.all()
    return render_to_response('rol/asignar_rol.html',
                              {'usuario_actor': usuario_actor, 'lista_usuarios': lista_usuarios},
                              context_instance=RequestContext(request))

@user_passes_test(User.can_change_user, login_url="/iniciar_sesion")
def asignar_rol(request, id_usuario):
    """
    :param request:
    :param idRol:
    :return:
    """
    usuario_actor = request.user
    usuario = User.objects.get(pk=id_usuario)
    if request.method == 'POST':
        formulario = AsignarRol(request.POST, instance=usuario)
        if formulario.is_valid():
           formulario.save()
           roles = Group.objects.all()
           return render_to_response('rol/operacion_rol_exito.html',
                                     {'mensaje': 'Rol asignado con exito', 'usuario_actor': usuario_actor,
                                      'roles': roles}, context_instance=RequestContext(request))
    else:
        formulario = AsignarRol(instance=usuario)
    return render(request, 'rol/form_rol.html', {'formulario': formulario,
                                                 'operacion': 'Seleccione el rol que desea asignar al usuario',
                                                 'usuario_actor': usuario_actor, 'usuario':usuario},
                  context_instance=RequestContext(request))


########################################################################################################################
#########################################Vista de credenciales##########################################################
########################################################################################################################
@login_required(login_url="/iniciar_sesion")
def administrar_credencial(request):
    """

    :param request:
    :return:
    """
    return render_to_response('credencial/administrar_credencial.html',{'usuario_actor':request.user}
                              ,context_instance=RequestContext(request))

########################################################################################################################
#########################################Vista de atributos#############################################################
########################################################################################################################

def administrar_atributo(request, id_proyecto):
    """

    :param request:
    :return:
    """
    usuario_actor = request.user
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    lista_atributos = Atributo.objects.filter(Proyecto=proyecto)
    return render_to_response('proyecto/atributo/administrar_atributo.html',
                              {'usuario_actor': usuario_actor, 'lista_atributos': lista_atributos,
                               'proyecto':proyecto},
                              context_instance=RequestContext(request))


@login_required(login_url="/iniciar_sesion")
def crear_atributo(request, id_proyecto):
    usuario_actor = request.user
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    atributo = Atributo(Usuario=usuario_actor, Proyecto=proyecto)
    if request.method == 'POST':
        formulario = AtributoForm(request.POST, instance=atributo)
        if formulario.is_valid():
            formulario.save()
            lista_atributos = Atributo.objects.filter(Proyecto=proyecto)
            return render_to_response('proyecto/atributo/atributo_exito.html',
                                      {'mensaje': 'El atributo se ha creado exitosamente',
                                       'usuario_actor': usuario_actor, 'lista_atributos':lista_atributos , 'proyecto': proyecto},
                                      context_instance=RequestContext(request))
    else:
        formulario = AtributoForm(instance=atributo)
    return render_to_response('proyecto/atributo/atributo_form.html',
                              {'formulario': formulario, 'operacion': 'Ingrese los datos del atributo',
                               'usuario_actor': usuario_actor, 'proyecto': proyecto},
                              context_instance=RequestContext(request))

@login_required(login_url="/iniciar_sesion")
def detalle_atributo(request, id_atributo, id_proyecto):
    """

    :param request:
    :param idRol:
    :return:
    """
    usuario_actor = request.user
    atributo = Atributo.objects.get(pk=id_atributo)
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    return render_to_response('proyecto/atributo/detalle_atributo.html',
                              {'usuario_actor': usuario_actor,
                               'atributo': atributo, 'proyecto': proyecto},
                              context_instance=RequestContext(request))


@login_required(login_url="/iniciar_sesion")
def modificar_atributo(request, id_proyecto, id_atributo):
    """

    :param request:
    :param id_proyecto:
    :param id_atributo:
    :return:
    """
    usuario_actor = request.user
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    lista_atributos = Atributo.objects.filter(Proyecto=proyecto)

    if proyecto.Estado == 'C':
                return render_to_response('proyecto/atributo/atributo_error.html',
                              {'usuario_actor': usuario_actor, 'proyecto': proyecto, 'lista_atributos': lista_atributos,
                               'mensaje': 'No puedes modificar los datos un atributo de un proyecto que ha sido cancelado'},
                              context_instance=RequestContext(request))
    else:
            if proyecto.Estado == 'F':
                return render_to_response('proyecto/atributo/atributo_error.html',
                              {'usuario_actor': usuario_actor, 'proyecto': proyecto, 'lista_atributos': lista_atributos,
                               'mensaje': 'No puedes modificar los datos un atributo de un proyecto que ha finalizado'},
                              context_instance=RequestContext(request))

    atributo = Atributo.objects.get(pk=id_atributo)
    if request.method == 'POST':
        formulario = AtributoForm(request.POST, instance=atributo)
        if formulario.is_valid():
            formulario.save()
            return render_to_response('proyecto/atributo/atributo_exito.html',
                                      {'mensaje': 'El atributo se ha modificado exitosamente',
                                       'usuario_actor': usuario_actor, 'proyecto':proyecto, 'atributo': atributo,
                                       'lista_atributos': lista_atributos},
                                      context_instance=RequestContext(request))
    else:
        formulario = AtributoForm(instance=atributo)
        return render_to_response('proyecto/atributo/atributo_form.html',
                              {'formulario': formulario, 'operacion': 'Modificar atributo',
                               'usuario_actor': usuario_actor,  'proyecto': proyecto, 'atributo': atributo},
                              context_instance=RequestContext(request))




@login_required(login_url="/iniciar_sesion")
def eliminar_atributo(request, id_atributo, id_proyecto):
    """

    :param request:
    :param idRol:
    :return:
    """
    atributo = Atributo.objects.get(pk=id_atributo)
    atributo.delete()
    usuario_actor = request.user
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    lista_atributos = Atributo.objects.filter(Proyecto=proyecto)
    return render_to_response('proyecto/atributo/atributo_exito.html',
                              {'usuario_actor': usuario_actor,'mensaje':'El atributo ha sido eliminado exitosamente',
                               'lista_atributos': lista_atributos ,  'proyecto':proyecto},
                              context_instance=RequestContext(request))


def confirmar_eliminar_atributo(request, id_atributo, id_proyecto):
    """

    :param request:
    :param idFase:
    :param id_proyecto:
    :return:
    """

    usuario_actor = request.user
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    lista_atributos = Atributo.objects.filter(Proyecto=id_proyecto)
    if proyecto.Estado == 'A':
                return render_to_response('proyecto/atributo/atributo_error.html',
                              {'usuario_actor': usuario_actor, 'proyecto': proyecto, 'lista_atributos': lista_atributos,
                               'mensaje': 'No puedes eliminar un atributo de un proyecto que ha iniciado'},
                              context_instance=RequestContext(request))
    else:
        if proyecto.Estado == 'C':
                return render_to_response('proyecto/atributo/atributo_error.html',
                              {'usuario_actor': usuario_actor, 'proyecto': proyecto, 'lista_atributos': lista_atributos,
                               'mensaje': 'No puedes eliminar un atributo de un proyecto que ha sido cancelado'},
                              context_instance=RequestContext(request))
        else:
            if proyecto.Estado == 'F':
                return render_to_response('proyecto/atributo/atributo_error.html',
                              {'usuario_actor': usuario_actor, 'proyecto': proyecto, 'lista_atributos': lista_atributos,
                               'mensaje': 'No puedes eliminar un atributo de un proyecto que ha finalizado'},
                              context_instance=RequestContext(request))
            else:
                atributo = Atributo.objects.get(pk=id_atributo)
                return render_to_response('proyecto/atributo/conf_eliminar_atributo.html',
                              {'usuario_actor': usuario_actor, 'atributo': atributo, 'proyecto': proyecto},
                              context_instance=RequestContext(request))

########################################################################################################################
########################################Vistas de tipo de item######################################################
########################################################################################################################

@login_required(login_url="/iniciar_sesion")
def administrar_tipoItem(request, id_proyecto):
    """

    :param request:
    :param id_proyecto:
    :return:
    """
    usuario_actor = request.user
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    lista_tipos = TipoDeItem.objects.filter(Proyecto=proyecto)
    return render_to_response('proyecto/tipoItem/administrar_tipoItem.html',
                              {'usuario_actor': usuario_actor, 'lista_tipos': lista_tipos,
                               'proyecto': proyecto},
                              context_instance=RequestContext(request))

@login_required(login_url="/iniciar_sesion")
def crear_tipoItem(request, id_proyecto):
    """

    :param request:
    :param id_proyecto:
    :return:
    """
    usuario_actor = request.user
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    tipo = TipoDeItem(Usuario=usuario_actor, Proyecto=proyecto)
    lista_tipos = TipoDeItem.objects.filter(Proyecto=proyecto)
    if request.method == 'POST':
        formulario = tipoItemForm(request.POST, instance=tipo)
        if formulario.is_valid():
            formulario.save()
            return render_to_response('proyecto/tipoItem/tipoItem_exito.html',
                                      {'mensaje': 'El tipo de item se ha creado exitosamente',
                                       'usuario_actor': usuario_actor, 'lista_tipos': lista_tipos,
                                       'proyecto': proyecto}, context_instance=RequestContext(request))
    else:
        formulario = tipoItemForm()
    return render_to_response('proyecto/tipoItem/tipoItem_form.html',
                              {'formulario': formulario, 'operacion': 'Ingrese los datos del tipo de item',
                               'usuario_actor': usuario_actor, 'proyecto': proyecto},
                              context_instance=RequestContext(request))

@login_required(login_url="/iniciar_sesion")
def detalle_tipoItem(request, id_tipo, id_proyecto):
    """
    :param request:
    :param id_tipo:
    :param id_proyecto:
    :return:
    """
    usuario_actor = request.user
    tipo = TipoDeItem.objects.get(pk=id_tipo)
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    return render_to_response('proyecto/tipoItem/detalle_tipoItem.html',
                              {'usuario_actor': usuario_actor,
                               'tipo': tipo, 'proyecto': proyecto},
                              context_instance=RequestContext(request))

@login_required(login_url="/iniciar_sesion")
def modificar_tipo(request, id_proyecto, id_tipo):
    """

    :param request:
    :param id_proyecto:
    :param id_tipo:
    :return:
    """
    usuario_actor = request.user
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    lista_tipos = TipoDeItem.objects.filter(Proyecto=proyecto)
    if proyecto.Estado == 'C':
                return render_to_response('proyecto/tipoItem/tipoItem_error.html',
                              {'usuario_actor': usuario_actor, 'proyecto': proyecto, 'lista_tipos': lista_tipos,
                               'mensaje': 'No puedes modificar los datos un tipo de item de un proyecto que ha sido cancelado'},
                              context_instance=RequestContext(request))
    else:
        if proyecto.Estado == 'F':
                return render_to_response('proyecto/tipoItem/tipoItem_error.html',
                              {'usuario_actor': usuario_actor, 'proyecto': proyecto, 'lista_tipos': lista_tipos,
                               'mensaje': 'No puedes modificar los datos un tipo de item de un proyecto que ha finalizado'},
                              context_instance=RequestContext(request))

    tipo = TipoDeItem.objects.get(pk=id_tipo)
    if request.method == 'POST':
        formulario = tipoItemForm(request.POST, instance=tipo)
        if formulario.is_valid():
            formulario.save()
            return render_to_response('proyecto/tipoItem/tipoItem_exito.html',
                                      {'mensaje': 'El atributo se ha modificado exitosamente',
                                       'usuario_actor': usuario_actor, 'proyecto':proyecto, 'tipo':tipo,
                                       'lista_tipos': lista_tipos},
                                      context_instance=RequestContext(request))
    else:
        formulario = tipoItemForm(instance=tipo)
    return render_to_response('proyecto/tipoItem/tipoItem_form.html',
                              {'formulario': formulario, 'operacion': 'Modificar tipo de item',
                               'usuario_actor': usuario_actor,  'proyecto':proyecto, 'tipo':tipo},
                              context_instance=RequestContext(request))

@login_required(login_url="/iniciar_sesion")
def eliminar_tipo(request, id_tipo, id_proyecto):
    """

    :param request:
    :param id_tipo:
    :param id_proyecto:
    :return:
    """
    tipo = TipoDeItem.objects.get(pk=id_tipo)
    tipo.delete()
    usuario_actor = request.user
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    lista_tipos = TipoDeItem.objects.filter(Proyecto=proyecto)
    return render_to_response('proyecto/tipoItem/tipoItem_exito.html',
                              {'usuario_actor': usuario_actor,'mensaje':'El tipo de item ha sido eliminado exitosamente',
                               'lista_tipos': lista_tipos, 'proyecto':proyecto},
                              context_instance=RequestContext(request))

def confirmar_eliminar_tipo(request, id_tipo, id_proyecto):
    """

    :param request:
    :param idFase:
    :param id_proyecto:
    :return:
    """

    usuario_actor = request.user
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    lista_tipos = TipoDeItem.objects.filter(Proyecto=id_proyecto)
    if proyecto.Estado == 'A':
                return render_to_response('proyecto/tipoItem/tipoItem_error.html',
                              {'usuario_actor': usuario_actor, 'proyecto': proyecto, 'lista_tipos': lista_tipos,
                               'mensaje': 'No puedes eliminar un tipo de item de un proyecto que ha iniciado'},
                              context_instance=RequestContext(request))
    else:
        if proyecto.Estado == 'C':
                return render_to_response('proyecto/tipoItem/tipoItem_error.html',
                              {'usuario_actor': usuario_actor, 'proyecto': proyecto, 'lista_tipos': lista_tipos,
                               'mensaje': 'No puedes eliminar un tipo de item de un proyecto que ha sido cancelado'},
                              context_instance=RequestContext(request))
        else:
            if proyecto.Estado == 'F':
                return render_to_response('proyecto/tipoItem/tipoItem_error.html',
                              {'usuario_actor': usuario_actor, 'proyecto': proyecto, 'lista_tipos': lista_tipos,
                               'mensaje': 'No puedes eliminar un tipo de item de un proyecto que ha finalizado'},
                              context_instance=RequestContext(request))
            else:
                tipo = TipoDeItem.objects.get(pk=id_tipo)
                return render_to_response('proyecto/tipoItem/conf_eliminar_tipo.html',
                              {'usuario_actor': usuario_actor, 'tipo': tipo, 'proyecto': proyecto},
                              context_instance=RequestContext(request))


