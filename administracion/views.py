# -*- encoding: utf-8 -*-
from django.contrib.auth import models
from django.shortcuts import render_to_response, render, HttpResponseRedirect, HttpResponse, RequestContext, get_object_or_404
from administracion.forms import *
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group , timezone
from administracion.models import Proyecto, Fase, Atributo, TipoDeItem
from django.contrib.auth.models import User, Group, Permission
from administracion.models import Proyecto, Fase
from desarrollo.models import Item
from django.db import IntegrityError


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
    usuario_actor = request.user
    lista_proyectos = Proyecto.objects.all().order_by('id')
    ctx = {'usuario_actor':usuario_actor,'lista_proyectos':lista_proyectos}
    return render_to_response('administracion.html', ctx, context_instance=RequestContext(request))
########################################################################################################################
#############################################Vistas de Administracion de Usuarios#######################################
########################################################################################################################

@user_passes_test( User.puede_consultar_usuarios , login_url="/iniciar_sesion")
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
    lista_usuarios = User.objects.all().order_by('id')
    ctx = {'usuario_actor':usuario_actor,'lista_usuarios':lista_usuarios}
    return render_to_response('usuario/administrar_usuario.html', ctx, context_instance=RequestContext(request))

@user_passes_test(User.puede_agregar_usuarios, login_url="/iniciar_sesion")
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
    lista_usuarios = User.objects.all().order_by('id')
    if request.method == 'POST':
        formulario = UserCreationForm(request.POST)
        if formulario.is_valid():
            usuario_creado = str(request.POST['username'])
            formulario.save()
            ctx = {'mensaje': 'El usuario '+usuario_creado + ' fue creado exitosamente', 'usuario_actor': usuario_actor,'lista_usuarios': lista_usuarios}
            return render_to_response('usuario/operacion_usuario_exito.html', ctx, context_instance=RequestContext(request))
    else:
        formulario = UserCreationForm()
        ctx = {'formulario': formulario, 'operacion': 'Ingrese los datos del nuevo usuario','usuario_actor': usuario_actor}
    return render_to_response('usuario/form_usuario.html', ctx, context_instance=RequestContext(request))

@user_passes_test(User.puede_modificar_usuarios, login_url="/iniciar_sesion")
def pass_change(request, id_usuario_p):
    usuario_parametro = User.objects.get(pk=id_usuario_p)
    lista_usuarios = User.objects.all().order_by('id')
    if request.method == 'POST':
        formulario = SetPasswordForm(data=request.POST, user=usuario_parametro)
        if formulario.is_valid():
           formulario.save()
           ctx = {'mensaje': 'Se ha actualizado la contraseña del usuario '+ str(usuario_parametro), 'usuario_actor': request.user, 'usuario_parametro': usuario_parametro,'lista_usuarios': lista_usuarios}
           return render_to_response('usuario/operacion_usuario_exito.html', ctx, context_instance=RequestContext(request))
    else:
        formulario = SetPasswordForm(user=usuario_parametro)
        ctx = {'usuario_actor': request.user, 'formulario': formulario, 'operacion': 'Cambio de contraseña', 'usuario_parametro': usuario_parametro}
    return render(request, 'usuario/form_usuario.html', ctx,context_instance=RequestContext(request))

@user_passes_test( User.puede_consultar_usuarios , login_url="/iniciar_sesion")
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


@user_passes_test( User.puede_eliminar_usuarios , login_url="/iniciar_sesion")
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
    if usuario_parametro.is_active == True:
        usuario_parametro.is_active = False
    else:
        usuario_parametro.is_active = True
    usuario_parametro.save()
    usuario_actor = request.user
    lista_usuarios = User.objects.all().order_by('id')
    return render_to_response('usuario/operacion_usuario_exito.html',
                                     {'mensaje': 'Cambio de estado de usuario '+str(usuario_parametro)+' con exito', 'usuario_actor':usuario_actor,
                                      'lista_usuarios': lista_usuarios}, context_instance=RequestContext(request))

########################################################################################################################
###########################################Vistas de Administrar Proyecto###############################################
########################################################################################################################


@user_passes_test( User.puede_agregar_proyectos , login_url="/iniciar_sesion")
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
        lista_proyectos = Proyecto.objects.all().order_by('id')
        formulario = ProyectoForm(request.POST, instance=proyecto)
        if formulario.is_valid():
            rolLiderProyecto = Group.objects.get(pk=2)
            lider = User.objects.get(pk=request.POST['Lider'])
            lider.groups.add(rolLiderProyecto)
            lider.save()
            formulario.save()
            proyecto_nombre = str(request.POST['Nombre'])

            return render_to_response('proyecto/proyecto_exito.html',
                                      {'mensaje': 'El proyecto '+proyecto_nombre+' ha sido creado exitosamente',
                                       'usuario_actor': usuario_actor, 'lista_proyectos': lista_proyectos},
                                      context_instance=RequestContext(request))
    else:
        formulario = ProyectoForm(instance=proyecto)
    return render_to_response('proyecto/crear_proyecto.html',
                              {'formulario': formulario, 'operacion':'Ingrese los datos del proyecto'
                               , 'usuario_actor': usuario_actor}, context_instance=RequestContext(request))

@user_passes_test( User.puede_consultar_proyectos, login_url="/iniciar_sesion")
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

@user_passes_test(User.puede_modificar_proyectos, login_url="/iniciar_sesion")
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
    lista_proyectos = Proyecto.objects.all().order_by('id')
    return render_to_response('proyecto/proyecto_exito.html', {'usuario_actor':request.user, 'proyecto':proyecto,
                              'mensaje': 'Se ha dado inicio al proyecto '+proyecto.Nombre, 'lista_proyectos': lista_proyectos}
                              ,context_instance=RequestContext(request))

@user_passes_test(User.puede_modificar_proyectos, login_url="/iniciar_sesion")
def confirmar_iniciar_proyecto(request, id_proyecto):
    """

    :param request:
    :param id_proyecto:
    :return:
    """
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    lista_proyectos = Proyecto.objects.all().order_by('id')
    if proyecto.Estado == 'A':
        return render_to_response('proyecto/proyecto_error.html', {'usuario_actor':request.user, 'proyecto':proyecto,
                              'mensaje': 'No puedes iniciar el proyecto '+proyecto.Nombre + ' porque ya ha sido iniciado, ver detalles',
                              'lista_proyectos': lista_proyectos}
                              ,context_instance=RequestContext(request))
    elif proyecto.Estado == 'C':
        return render_to_response('proyecto/proyecto_error.html', {'usuario_actor':request.user, 'proyecto':proyecto,
                              'mensaje': 'No puedes iniciar el proyecto '+proyecto.Nombre + ' porque  ya ha sido cancelado, ver detalles',
                              'lista_proyectos': lista_proyectos}
                              ,context_instance=RequestContext(request))
    elif proyecto.Estado == 'F':
        return render_to_response('proyecto/proyecto_error.html', {'usuario_actor':request.user, 'proyecto':proyecto,
                              'mensaje': 'No puedes iniciar el proyecto '+proyecto.Nombre + ' porque  ya ha finalizado, ver detalles',
                              'lista_proyectos': lista_proyectos}
                              ,context_instance=RequestContext(request))
    elif proyecto.nFases == 0:
        return render_to_response('proyecto/proyecto_error.html', {'usuario_actor':request.user, 'proyecto':proyecto,
                              'mensaje': 'No puedes iniciar el proyecto '+proyecto.Nombre + ' porque no tiene fase alguna, ver detalles',
                              'lista_proyectos': lista_proyectos}
                              ,context_instance=RequestContext(request))
    else:
        lista_fase = Fase.objects.filter(Proyecto=proyecto)
        for fase in lista_fase:
            lista_tipo = TipoDeItem.objects.filter(Fase=fase)
            if not lista_tipo.exists():
                return render_to_response('proyecto/proyecto_error.html', {'usuario_actor':request.user, 'proyecto':proyecto,
                              'mensaje': 'No puedes iniciar el proyecto '+proyecto.Nombre + ' porque la fase '+fase.Nombre+' no tiene tipo de item algun',
                              'lista_proyectos': lista_proyectos}
                              ,context_instance=RequestContext(request))

    return render_to_response('proyecto/conf_iniciar_proyecto.html', {'usuario_actor': request.user, 'proyecto': proyecto
                                ,'lista_proyectos': lista_proyectos}, context_instance=RequestContext(request))


@user_passes_test(User.puede_eliminar_proyectos, login_url="/iniciar_sesion")
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
    lista_proyectos = Proyecto.objects.all().order_by('id')
    return render_to_response('proyecto/proyecto_exito.html', {'usuario_actor':request.user, 'proyecto':proyecto,
                              'mensaje': 'Se ha cancelado el proyecto'+proyecto.Nombre, 'lista_proyectos':lista_proyectos}
                              ,context_instance=RequestContext(request))

@user_passes_test(User.puede_eliminar_proyectos, login_url="/iniciar_sesion")
def confirmar_eliminar_proyecto(request, id_proyecto):
    """

    :param request:
    :param id_proyecto:
    :return:
    """
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    lista_proyectos = Proyecto.objects.all().order_by('id')

    if proyecto.Estado == 'C':
        return render_to_response('proyecto/proyecto_error.html', {'usuario_actor':request.user, 'proyecto':proyecto,
                              'mensaje': 'No puedes cancelar el proyecto '+proyecto.Nombre + ' porque ya ha sido cancelado, ver detalles',
                              'lista_proyectos': lista_proyectos}
                              ,context_instance=RequestContext(request))
    else:
        return render_to_response('proyecto/conf_eliminar_proyecto.html', {'usuario_actor': request.user, 'proyecto': proyecto
                                , 'lista_proyectos': lista_proyectos}, context_instance=RequestContext(request))

@user_passes_test(User.puede_modificar_proyectos, login_url="/iniciar_sesion")
def modificar_proyecto(request, id_proyecto):
    """

    :param request:
    :param id_proyecto:
    :return:
    """
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    LiderAntiguo = proyecto.Lider
    lista_proyectos = Proyecto.objects.all().order_by('id')

    if proyecto.Estado == 'P':
        if request.method == 'POST':
            formulario = ProyectoForm(request.POST, instance=proyecto)
            if formulario.is_valid():
                rolLiderProyecto=Group.objects.get(pk=2)
                if Proyecto.objects.filter(Lider=LiderAntiguo).count() == 1:
                    LiderAntiguo.groups.remove(rolLiderProyecto)
                    LiderAntiguo.save()
                lider = User.objects.get(pk=request.POST['Lider'])
                lider.groups.add(rolLiderProyecto)
                lider.save()
                formulario.save()
                return render_to_response('proyecto/proyecto_exito.html',
                                      {'mensaje': 'El proyecto '+proyecto.Nombre+' ha sido modificado exitosamente',
                                       'usuario_actor': request.user, 'lista_proyectos': lista_proyectos},
                                      context_instance=RequestContext(request))
            else:
                return render_to_response('proyecto/crear_proyecto.html',
                              {'formulario': formulario, 'operacion': 'Ingrese los datos del proyecto '+proyecto.Nombre
                               , 'usuario_actor': request.user}, context_instance=RequestContext(request))
        else:
            formulario = ProyectoForm(instance=proyecto)
            return render_to_response('proyecto/crear_proyecto.html',
                              {'formulario': formulario, 'operacion': 'Ingrese los datos del proyecto '+proyecto.Nombre
                               , 'usuario_actor': request.user}, context_instance=RequestContext(request))
    elif proyecto.Estado == 'C':
            return render_to_response('proyecto/proyecto_error.html',
                                      {'mensaje': 'No puedes modificar los datos del proyecto '+proyecto.Nombre + ' porque ya ha sido cancelado, ver detalles',
                                       'usuario_actor': request.user, 'lista_proyectos': lista_proyectos},
                                      context_instance=RequestContext(request))
    elif proyecto.Estado == 'A':
            return render_to_response('proyecto/proyecto_error.html',
                                      {'mensaje': 'No puedes modificar los datos del proyecto '+proyecto.Nombre + ' porque ya ha iniciado, ver detalles',
                                       'usuario_actor': request.user, 'lista_proyectos': lista_proyectos},
                                      context_instance=RequestContext(request))
    elif proyecto.Estado == 'F':
            return render_to_response('proyecto/proyecto_error.html',
                                      {'mensaje': 'No puedes modificar los datos del proyecto '+proyecto.Nombre + ' porque ya ha finalizado, ver detalles',
                                       'usuario_actor': request.user, 'lista_proyectos': lista_proyectos},
                                      context_instance=RequestContext(request))

@user_passes_test(User.puede_modificar_proyectos, login_url="/iniciar_sesion")
def modificar_proyecto_lider(request, id_proyecto):
    """

    :param request:
    :param id_proyecto:
    :return:
    """
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    lista_proyectos = Proyecto.objects.all().order_by('id')

    if proyecto.Estado == 'P':
        if request.method == 'POST':
            formulario = ProyectoFormLider(request.POST, instance=proyecto)
            if formulario.is_valid():
                formulario.save()
                return render_to_response('proyecto/proyecto_exito.html',
                                      {'mensaje': 'El proyecto '+proyecto.Nombre+' ha sido modificado exitosamente',
                                       'usuario_actor': request.user, 'lista_proyectos': lista_proyectos},
                                      context_instance=RequestContext(request))
            else:
                return render_to_response('proyecto/crear_proyecto.html',
                              {'formulario': formulario, 'operacion': 'Ingrese los datos del proyecto '+proyecto.Nombre
                               , 'usuario_actor': request.user}, context_instance=RequestContext(request))
        else:
            formulario = ProyectoFormLider(instance=proyecto)
            return render_to_response('proyecto/crear_proyecto.html',
                              {'formulario': formulario, 'operacion': 'Ingrese los datos del proyecto '+proyecto.Nombre
                               , 'usuario_actor': request.user}, context_instance=RequestContext(request))
    elif proyecto.Estado == 'C':
            return render_to_response('proyecto/proyecto_error.html',
                                      {'mensaje': 'No puedes modificar los datos del proyecto '+proyecto.Nombre + ' porque ya ha sido cancelado, ver detalles',
                                       'usuario_actor': request.user, 'lista_proyectos': lista_proyectos},
                                      context_instance=RequestContext(request))
    elif proyecto.Estado == 'A':
            return render_to_response('proyecto/proyecto_error.html',
                                      {'mensaje': 'No puedes modificar los datos del proyecto '+proyecto.Nombre + ' porque ya ha iniciado, ver detalles',
                                       'usuario_actor': request.user, 'lista_proyectos': lista_proyectos},
                                      context_instance=RequestContext(request))
    elif proyecto.Estado == 'F':
            return render_to_response('proyecto/proyecto_error.html',
                                      {'mensaje': 'No puedes modificar los datos del proyecto '+proyecto.Nombre + ' porque ya ha finalizado, ver detalles',
                                       'usuario_actor': request.user, 'lista_proyectos': lista_proyectos},
                                      context_instance=RequestContext(request))

@user_passes_test(User.puede_modificar_proyectos, login_url="/iniciar_sesion")
def proyecto_asignar_usuarios(request, id_proyecto):
    """

    :param request:
    :param id_proyecto:
    :return:
    """
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    lista_proyectos = Proyecto.objects.all().order_by('id')

    if proyecto.Estado == 'A':
        if request.method == 'POST':
            formulario = ProyectoAsignarUsuarioForm(request.POST, instance=proyecto)
            formulario.fields["Usuarios"].queryset = User.objects.exclude(pk=1).exclude(pk=request.user.pk)
            if formulario.is_valid():
                formulario.save()
                return render_to_response('proyecto/proyecto_exito.html',
                                      {'mensaje': 'El proyecto '+proyecto.Nombre+' ha sido modificado exitosamente',
                                       'usuario_actor': request.user, 'lista_proyectos': lista_proyectos},
                                      context_instance=RequestContext(request))
            else:
                formulario.fields["Usuarios"].queryset = User.objects.exclude(pk=1).exclude(pk=request.user.pk)
                formulario.fields["Usuarios"].help_text = "Haga doble click en el Usuario que desee agregar al proyecto"
                return render_to_response('proyecto/crear_proyecto.html',
                              {'formulario': formulario, 'operacion': 'Usuarios que participaran en el proyecto '+proyecto.Nombre
                               , 'usuario_actor': request.user}, context_instance=RequestContext(request))
        else:
            formulario = ProyectoAsignarUsuarioForm(instance=proyecto)
            formulario.fields["Usuarios"].queryset = User.objects.exclude(pk=1).exclude(pk=request.user.pk)
            formulario.fields["Usuarios"].help_text = "Haga doble click en el Usuario que desee agregar al proyecto"
            return render_to_response('proyecto/crear_proyecto.html',
                              {'formulario': formulario, 'operacion': 'Usuarios que participaran en el proyecto '+proyecto.Nombre
                               , 'usuario_actor': request.user}, context_instance=RequestContext(request))
    elif proyecto.Estado == 'C':
            return render_to_response('proyecto/proyecto_error.html',
                                      {'mensaje': 'No puedes modificar los datos del proyecto '+proyecto.Nombre + ' porque ya ha sido cancelado, ver detalles',
                                       'usuario_actor': request.user, 'lista_proyectos': lista_proyectos},
                                      context_instance=RequestContext(request))

    elif proyecto.Estado == 'F':
            return render_to_response('proyecto/proyecto_error.html',
                                      {'mensaje': 'No puedes modificar los datos del proyecto '+proyecto.Nombre + ' porque ya ha finalizado, ver detalles',
                                       'usuario_actor': request.user, 'lista_proyectos': lista_proyectos},
                                      context_instance=RequestContext(request))
def confirmar_finalizar_proyecto(request, id_proyecto):
    """

    :param request:
    :param id_proyecto:
    :return:
    """
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    usuario = request.user
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    lista_proyectos = Proyecto.objects.all().order_by('id')
    lista_fases = Fase.objects.filter(Proyecto=proyecto)

    if lista_fases.exclude(Estado=Fase.FINALIZADA).exists():
        return render_to_response('proyecto/proyecto_error.html', {'usuario_actor':request.user, 'proyecto':proyecto,
                              'mensaje': 'No puedes finalizar el proyecto '+proyecto.Nombre + ' porque no todas sus bases han finalizado',
                              'lista_proyectos': lista_proyectos}
                              ,context_instance=RequestContext(request))
    else:
        return render_to_response('proyecto/conf_finalizar_proyecto.html', {'usuario_actor': request.user, 'proyecto': proyecto
                                , 'lista_proyectos': lista_proyectos}, context_instance=RequestContext(request))


def finalizar_proyecto_view(request, id_proyecto):
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    usuario = request.user
    lista_proyectos =  Proyecto.objects.all().order_by('id')
    proyecto.Estado = 'F'
    proyecto.save()
    return render_to_response('proyecto/proyecto_exito.html',
                                      {'mensaje': 'Se ha finalizado el proyecto '+proyecto.Nombre,
                                       'usuario_actor': request.user, 'lista_proyectos': lista_proyectos},
                                      context_instance=RequestContext(request))




########################################################################################################################
###########################################Vistas de administracion de Fase#############################################
########################################################################################################################

@user_passes_test(User.puede_consultar_fases, login_url="/iniciar_sesion")
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
    lista_fases = Fase.objects.filter(Proyecto=id_proyecto).order_by('Numero')
    return render_to_response('proyecto/fase/adm-fases.html',
                              {'usuario_actor': usuario_actor, 'lista_fases': lista_fases, 'proyecto': proyecto}
                              , context_instance=RequestContext(request))

@user_passes_test(User.puede_modificar_fases, login_url="/iniciar_sesion")
def ordenar_fase_subir(request, id_fase):
    """

    :param request:
    :param id_fase:
    :return:
    """
    fase = Fase.objects.get(pk=id_fase)
    usuario_actor = request.user
    proyecto = Proyecto.objects.get(pk=fase.Proyecto.id)
    lista_fases = Fase.objects.filter(Proyecto=fase.Proyecto.id).order_by('Numero')
    if fase.Proyecto.Estado == 'P':
        fase.ordenar_fase_subir()
        return administrar_fases(request,fase.Proyecto.id)
    else:
        return render_to_response('proyecto/fase/fases_error.html',
                              {'usuario_actor': usuario_actor, 'lista_fases': lista_fases,
                               'proyecto': proyecto,'mensaje': 'Solo puedes cambiar el orden de las fases en proyectos con estado PENDINTE'}
                              , context_instance=RequestContext(request))

@user_passes_test(User.puede_modificar_fases, login_url="/iniciar_sesion")
def ordenar_fase_bajar(request, id_fase):
    """

    :param request:
    :param id_fase:
    :return:
    """
    usuario_actor = request.user
    fase = Fase.objects.get(pk=id_fase)
    proyecto = Proyecto.objects.get(pk=fase.Proyecto.id)
    lista_fases = Fase.objects.filter(Proyecto=fase.Proyecto.id).order_by('Numero')
    if fase.Proyecto.Estado == 'P':
        fase.ordenar_fase_bajar()
        return administrar_fases(request,fase.Proyecto.id)
    else:
        return render_to_response('proyecto/fase/fases_error.html',
                              {'usuario_actor': usuario_actor, 'lista_fases': lista_fases,
                               'proyecto': proyecto,'mensaje': 'Solo puedes cambiar el orden de las fases en proyectos con estado PENDINTE'}
                              , context_instance=RequestContext(request))

@user_passes_test(User.puede_agregar_fases, login_url="/iniciar_sesion")
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
    lista_fases = Fase.objects.filter(Proyecto=proyecto).order_by('Numero')
    if proyecto.Estado == 'A':
                return render_to_response('proyecto/fase/fases_error.html',
                              {'usuario_actor': usuario_actor, 'proyecto': proyecto, 'lista_fases': lista_fases,
                               'mensaje': 'No puedes crear una fase a un proyecto que ha iniciado'},
                              context_instance=RequestContext(request))
    elif proyecto.Estado == 'C':
                return render_to_response('proyecto/fase/fases_error.html',
                              {'usuario_actor': usuario_actor, 'proyecto': proyecto, 'lista_fases': lista_fases,
                               'mensaje': 'No puedes crear una fase a un proyecto que ha sido cancelado'},
                              context_instance=RequestContext(request))
    elif proyecto.Estado == 'F':
                return render_to_response('proyecto/fase/fases_error.html',
                              {'usuario_actor': usuario_actor, 'proyecto': proyecto, 'lista_fases': lista_fases,
                               'mensaje': 'No puedes crear una fase a un proyecto que ha finalizado'},
                              context_instance=RequestContext(request))
    elif request.method == 'POST':
        fase.Numero = 0
        formulario = FaseForm(request.POST, instance=fase)
        if formulario.is_valid():
            proyecto.nFases += 1
            fase.Numero = proyecto.nFases
            formulario = FaseForm(request.POST, instance=fase)
            try:
                formulario.save()
            except IntegrityError:
                mensaje= 'No se puede crear la fase con el nombre elegido ya que esta siendo usado por otra'
                return render_to_response('proyecto/fase/fase_form.html',
                              {'usuario_actor': usuario_actor, 'formulario': formulario, 'proyecto': proyecto,'error':True,'mensaje':mensaje,
                               'operacion':'Ingrese los datos de la fase'},
                              context_instance=RequestContext(request))

            proyecto.save()
            fase_nombre = str(request.POST['Nombre'])
            return render_to_response('proyecto/fase/fases_exito.html',
                              {'usuario_actor': usuario_actor, 'proyecto': proyecto, 'lista_fases': lista_fases,
                               'mensaje': 'Se ha creado la fase '+fase_nombre+' exitosamente'},
                              context_instance=RequestContext(request))
    else:
        formulario = FaseForm(instance=fase)
    return render_to_response('proyecto/fase/fase_form.html',
                              {'usuario_actor': usuario_actor, 'formulario': formulario, 'proyecto': proyecto,
                               'operacion':'Ingrese los datos de la fase'},
                              context_instance=RequestContext(request))



def iniciar_fase(request, id_proyecto, id_fase):
    """

    :param request:
    :param id_proyecto:
    :return:
    """
    fase = Fase.objects.get(pk=id_fase)
    fase.Estado = Fase.INICIADA
    #fase.Fecha_inicio = timezone.now()
    fase.save()
    proyecto = fase.Proyecto

    lista_fases = Fase.objects.filter(Proyecto=id_proyecto).order_by('Numero')
    return render_to_response('proyecto/fase/fases_exito.html', {'usuario_actor':request.user, 'fase':fase,'proyecto':proyecto,
                              'mensaje': 'Se ha dado inicio a la fase '+fase.Nombre, 'lista_fases': lista_fases}
                              ,context_instance=RequestContext(request))

def confirmar_iniciar_fase(request, id_proyecto, id_fase):
    """

    :param request:
    :param id_proyecto:
    :return:
    """
    fase = Fase.objects.get(pk=id_fase)
    lista_fases = Fase.objects.filter(Proyecto=id_proyecto).order_by('Numero')
    proyecto = fase.Proyecto

    if fase.Proyecto.Estado == 'C':
        return render_to_response('proyecto/fase/fases_error.html', {'usuario_actor':request.user, 'fase': fase, 'proyecto':proyecto,
                              'mensaje': 'No puedes iniciar la fase '+fase.Nombre + ' porque el proyecto ya ha sido cancelado, ver detalles',
                              'lista_fases': lista_fases}
                              ,context_instance=RequestContext(request))
    elif fase.Proyecto.Estado == 'F':
        return render_to_response('proyecto/fase/fases_error.html', {'usuario_actor':request.user, 'fase':fase,'proyecto':proyecto,
                              'mensaje': 'No puedes iniciar la fase '+fase.Nombre + ' porque el proyecto ya ha finalizado, ver detalles',
                              'lista_fases': lista_fases}
                              ,context_instance=RequestContext(request))
    elif fase.Numero > 1:
        fase_anterior = Fase.objects.get(Proyecto=fase.Proyecto, Numero=(fase.Numero-1))
        lista_item = Item.objects.filter(Fase=fase_anterior).filter(Estado=Item.VALIDADO)
        if not lista_item:
            return render_to_response('proyecto/fase/fases_error.html', {'usuario_actor':request.user, 'fase':fase,'proyecto':proyecto,
                            'mensaje': 'No puedes iniciar la fase '+fase.Nombre + ' porque la fase anterior no posee ningun item en linea base',
                              'lista_fases': lista_fases}, context_instance=RequestContext(request))

    elif not fase.Usuarios.exists():
            return render_to_response('proyecto/fase/fases_error.html', {'usuario_actor':request.user, 'fase':fase,'proyecto':proyecto,
                            'mensaje': 'No puedes iniciar la fase '+fase.Nombre + ' porque la fase anterior no has asignado ningun usuario a ella',
                              'lista_fases': lista_fases}, context_instance=RequestContext(request))

    mensaje = 'Estas seguro que desea iniciar la fase '+fase.Nombre+' este cambio es irrevertible'
    return render_to_response('proyecto/fase/conf_iniciar_fase.html', {'usuario_actor': request.user, 'fase': fase
                                ,'lista_fases': lista_fases, 'mensaje':mensaje}, context_instance=RequestContext(request))


def finalizar_fase(request, id_proyecto, id_fase):
    """

    :param request:
    :param id_proyecto:
    :return:
    """

    fase = Fase.objects.get(pk=id_fase)
    fase.Estado = Fase.FINALIZADA
    #fase.Fecha_inicio = timezone.now()
    fase.save()
    proyecto = fase.Proyecto

    lista_fases = Fase.objects.filter(Proyecto=id_proyecto).order_by('Numero')
    return render_to_response('proyecto/fase/fases_exito.html', {'usuario_actor':request.user, 'fase':fase,'proyecto':proyecto,
                              'mensaje': 'Se ha finalizado a la fase '+fase.Nombre, 'lista_fases': lista_fases}
                              ,context_instance=RequestContext(request))

def confirmar_finalizar_fase(request, id_proyecto, id_fase):

    """
    :param request:
    :param id_proyecto:
    :return:
    """

    fase = Fase.objects.get(pk=id_fase)
    lista_fases = Fase.objects.filter(Proyecto=id_proyecto).order_by('Numero')
    proyecto = fase.Proyecto
    lista_items = Item.objects.filter(Fase=fase).exclude(condicion=Item.ELIMINADO)

    if fase.Proyecto.Estado == 'C':
        return render_to_response('proyecto/fase/fases_error.html', {'usuario_actor':request.user, 'fase': fase, 'proyecto':proyecto,
                              'mensaje': 'No puedes finalizar la fase '+fase.Nombre + ' porque el proyecto ya ha sido cancelado, ver detalles',
                              'lista_fases': lista_fases}
                              ,context_instance=RequestContext(request))
    elif fase.Proyecto.Estado == 'F':
        return render_to_response('proyecto/fase/fases_error.html', {'usuario_actor':request.user, 'fase':fase,'proyecto':proyecto,
                              'mensaje': 'No puedes finalizar la fase '+fase.Nombre + ' porque el proyecto ya ha finalizado, ver detalles',
                              'lista_fases': lista_fases}
                              ,context_instance=RequestContext(request))

    elif not lista_items.exists():
        return render_to_response('proyecto/fase/fases_error.html', {'usuario_actor':request.user, 'fase':fase,'proyecto':proyecto,
                              'mensaje': 'No puedes finalizar la fase '+fase.Nombre + ' porque no posee item alguno',
                              'lista_fases': lista_fases}, context_instance=RequestContext(request))

    elif lista_items.exclude(Estado=Item.VALIDADO).exists():
        return render_to_response('proyecto/fase/fases_error.html', {'usuario_actor':request.user, 'fase':fase,'proyecto':proyecto,
                              'mensaje': 'No puedes finalizar la fase '+fase.Nombre + ' porque no posee item alguno en lina base',
                              'lista_fases': lista_fases}, context_instance=RequestContext(request))
    elif fase.Numero > 1:
        fase_anterior = Fase.objects.get(Proyecto=fase.Proyecto, Numero=(fase.Numero-1))
        if not fase_anterior.FINALIZADA:
            return render_to_response('proyecto/fase/fases_error.html', {'usuario_actor':request.user, 'mensaje': 'No puedes iniciar la fase '+fase.Nombre + ' porque no todos los items estan en una linea base, ver detalles',
                                'fase':fase,'proyecto':proyecto,
                              'lista_fases': lista_fases}, context_instance=RequestContext(request))

    mensaje = 'Estas seguro que desea finalizar la fase '+fase.Nombre+' este cambio es irrevertible'
    return render_to_response('proyecto/fase/conf_finalizar_fase.html', {'usuario_actor': request.user, 'fase': fase
                                ,'lista_fases': lista_fases, 'mensaje':mensaje}, context_instance=RequestContext(request))



@user_passes_test(User.puede_consultar_fases, login_url="/iniciar_sesion")
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

@user_passes_test(User.puede_modificar_fases, login_url="/iniciar_sesion")
def modificar_fase(request, idFase, id_proyecto):
    """
    :param request:
    :param idFase:
    :param id_proyecto:
    :return:
    """
    usuario_actor = request.user
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    lista_fases = Fase.objects.filter(Proyecto=id_proyecto).order_by('Numero')
    fase = Fase.objects.get(pk=idFase)

    if proyecto.Estado == 'A':
                return render_to_response('proyecto/fase/fases_error.html',
                              {'usuario_actor': usuario_actor, 'proyecto': proyecto, 'lista_fases': lista_fases,
                               'mensaje': 'No puedes modificar los datos de una fase de un proyecto que ha iniciado'},
                              context_instance=RequestContext(request))
    elif proyecto.Estado == 'C':
                return render_to_response('proyecto/fase/fases_error.html',
                              {'usuario_actor': usuario_actor, 'proyecto': proyecto, 'lista_fases': lista_fases,
                               'mensaje': 'No puedes modificar los datos de una fase de un proyecto que ha sido cancelado'},
                              context_instance=RequestContext(request))
    elif proyecto.Estado == 'F':
                return render_to_response('proyecto/fase/fases_error.html',
                              {'usuario_actor': usuario_actor, 'proyecto': proyecto, 'lista_fases': lista_fases,
                               'mensaje': 'No puedes modificar los datos de una fase de un proyecto que ha finalizado'},
                              context_instance=RequestContext(request))
    elif request.method == 'POST':
        formulario = FaseForm(request.POST, instance=fase)
        if formulario.is_valid():
           formulario.save()
           return render_to_response('proyecto/fase/fases_exito.html',
                              {'usuario_actor': usuario_actor, 'proyecto': proyecto, 'lista_fases': lista_fases,
                               'mensaje': 'Se ha modificado la fase '+fase.Nombre+' exitosamente'},
                              context_instance=RequestContext(request))
        else:
            return render_to_response('proyecto/fase/fase_form.html',
                              {'usuario_actor': usuario_actor, 'formulario': formulario, 'proyecto': proyecto,
                               'fase': fase, 'operacion': 'Modificar Fase'}, context_instance=RequestContext(request))
    else:
        formulario = FaseForm(instance=fase)
        return render_to_response('proyecto/fase/fase_form.html',
                              {'usuario_actor': usuario_actor, 'formulario': formulario, 'proyecto': proyecto,
                               'fase': fase, 'operacion': 'Modificar Fase'}, context_instance=RequestContext(request))

@user_passes_test(User.puede_eliminar_fases, login_url="/iniciar_sesion")
def confirmar_eliminar_fase(request, idFase, id_proyecto):
    """

    :param request:
    :param idFase:
    :param id_proyecto:
    :return:
    """
    usuario_actor = request.user
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    lista_fases = Fase.objects.filter(Proyecto=id_proyecto).order_by('Numero')
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


@user_passes_test(User.puede_eliminar_fases, login_url="/iniciar_sesion")
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
    fase_nombre = fase.Nombre
    reordenar(proyecto.id, fase.Numero)
    fase.delete()
    lista_fases = Fase.objects.filter(Proyecto=id_proyecto).order_by('Numero')

    return render_to_response('proyecto/fase/fases_exito.html',
                              {'usuario_actor': usuario_actor, 'proyecto': proyecto, 'lista_fases': lista_fases,
                               'mensaje': 'La fase '+fase_nombre+' ha sido eliminada exitosamente'},
                              context_instance=RequestContext(request))

def reordenar(idproyecto, numero):
    proyecto = Proyecto.objects.get(pk=idproyecto)
    for n in range(numero+1, proyecto.nFases+2, 1):
        fase = Fase.objects.get(Proyecto=proyecto, Numero=n)
        fase.Numero-=1
        fase.save()
    return True

@user_passes_test(User.puede_modificar_fases, login_url="/iniciar_sesion")
def fase_asignar_usuarios(request, id_proyecto, idFase):
    '''

    :param request:
    :param id_proyecto:
    :param id_fase:
    :return:
    '''
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    lista_fases = Fase.objects.filter(Proyecto=proyecto).order_by('Numero')
    fase = Fase.objects.get(pk=idFase)

    if proyecto.Estado == 'A':
        if request.method == 'POST':
            formulario = AsignarUsuarioFase(request.POST, instance=fase)
            if formulario.is_valid():
                formulario.save()
                return render_to_response('proyecto/fase/fases_exito.html',
                                      {'mensaje': 'La fase '+fase.Nombre+' ha sido modificado exitosamente',
                                       'usuario_actor': request.user, 'lista_fases': lista_fases, 'proyecto': proyecto},
                                      context_instance=RequestContext(request))
            else:
                formulario.fields["Usuarios"].queryset = proyecto.Usuarios.all()
                formulario.fields["Usuarios"].help_text = "Haga doble click en el Usuario que desee agregar a la fase"
                return render_to_response('proyecto/fase/fase_form.html',
                              {'formulario': formulario, 'operacion': 'Usuarios que participaran en la fase '+fase.Nombre
                               , 'usuario_actor': request.user, 'proyecto': proyecto}, context_instance=RequestContext(request))
        else:
            formulario = AsignarUsuarioFase(instance=fase)
            formulario.fields["Usuarios"].queryset = proyecto.Usuarios.all()
            formulario.fields["Usuarios"].help_text = "Haga doble click en el Usuario que desee agregar a la fase"
            return render_to_response('proyecto/fase/fase_form.html',
                              {'formulario': formulario, 'operacion': 'Usuarios que participaran en la fase '+fase.Nombre
                               , 'usuario_actor': request.user, 'proyecto': proyecto}, context_instance=RequestContext(request))
    elif proyecto.Estado == 'C':
            return render_to_response('proyecto/fase/fases_error.html',
                                      {'mensaje': 'No puedes modificar los datos de la fase '+fase.Nombre + ' porque el proyecto ya ha sido cancelado, ver detalles',
                                       'usuario_actor': request.user, 'lista_fases': lista_fases, 'proyecto': proyecto},
                                      context_instance=RequestContext(request))
    elif proyecto.Estado == 'F':
            return render_to_response('proyecto/fase/fases_error.html',
                                      {'mensaje': 'No puedes modificar los datos de la fase '+fase.Nombre + ' porque el proyecto ya ha finalizado, ver detalles',
                                       'usuario_actor': request.user, 'lista_fases': lista_fases, 'proyecto': proyecto},
                                      context_instance=RequestContext(request))

########################################################################################################################
###########################################Vistas de administracion de Rol##############################################
########################################################################################################################
@user_passes_test(User.puede_consultar_roles, login_url="/iniciar_sesion")
def administrar_roles(request, id_proyecto):
    """

    :param request:
    :return:
    """
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    usuario_actor = request.user
    lista_usuarios = proyecto.Usuarios.all().order_by('pk')
    return render_to_response('proyecto/rol/administrar_rol.html',
                              {'usuario_actor': usuario_actor, 'lista_usuarios': lista_usuarios, 'proyecto':proyecto}
                              , context_instance=RequestContext(request))

@user_passes_test(User.puede_consultar_roles, login_url="/iniciar_sesion")
def listar_roles(request, id_proyecto):
    """

    :param request:
    :return:
    """
    usuario_actor = request.user
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    roles = Group.objects.filter(Proyecto=proyecto)
    return render_to_response('proyecto/rol/listar_roles.html',
                              {'usuario_actor': usuario_actor, 'roles': roles, 'proyecto':proyecto}
                              , context_instance=RequestContext(request))

@user_passes_test(User.puede_agregar_roles, login_url="/iniciar_sesion")
def crear_rol(request, id_proyecto):
    """

    :param request:
    :return:
    """
    mensaje="Rol creado con exito"
    proyecto= Proyecto.objects.get(pk=id_proyecto)
    usuario_actor = request.user
    lista_usuarios = proyecto.Usuarios
    rol = Group(Usuario=usuario_actor, Proyecto=proyecto)
    roles = Group.objects.filter(Proyecto=proyecto)
    if request.method == 'POST':
        formulario = RolForm(request.POST, instance=rol)
        formulario.fields["permissions"].queryset = Permission.objects.filter(content_type=12)
        if formulario.is_valid():
            formulario.save()
            return render_to_response('proyecto/rol/rol_exito.html',
                                      {'mensaje': mensaje, 'usuario_actor': usuario_actor,
                                       'lista_usuarios': lista_usuarios, 'roles': roles, 'proyecto':proyecto},
                                      context_instance=RequestContext(request))
    else:
        formulario = RolForm(instance=rol)
        formulario.fields["permissions"].queryset = Permission.objects.filter(content_type=12)
    return render_to_response('proyecto/rol/crear_rol.html',
                              {'formulario': formulario, 'operacion': 'Ingrese los datos del rol a crear',
                               'usuario_actor': usuario_actor, 'proyecto':proyecto},
                              context_instance=RequestContext(request))

@user_passes_test(User.puede_consultar_roles, login_url="/iniciar_sesion")
def detalle_rol(request, id_proyecto, idRol):
    """

    :param request:
    :param idRol:
    :return:
    """
    usuario_actor = request.user
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    rol = Group.objects.get(pk=idRol)
    lista_permisos = rol.permissions.all()
    return render_to_response('proyecto/rol/detallerol.html', {'usuario_actor': usuario_actor, 'rol': rol,
                                                      'lista_permisos': lista_permisos, 'proyecto':proyecto},
                              context_instance=RequestContext(request))

@user_passes_test(User.puede_modificar_roles, login_url="/iniciar_sesion")
def modificar_rol(request, id_proyecto, idRol):
    """

    :param request:
    :param idRol:
    :return:
    """
    usuario_actor = request.user
    rol = Group.objects.get(pk=idRol)
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    roles = Group.objects.filter(Proyecto=proyecto).order_by('id')
    lista_usuarios = proyecto.Usuarios.all()
    formulario = RolForm(request.POST, instance=rol)
    formulario.fields["permissions"].queryset = Permission.objects.filter(content_type=12)
    if formulario.is_valid():
        formulario.save()
        mensaje = 'El rol ha sido modificado exitosamente'
        return render_to_response('proyecto/rol/rol_exito.html',
                                      {'mensaje': mensaje, 'usuario_actor': usuario_actor,
                                       'lista_usuarios': lista_usuarios, 'roles': roles, 'proyecto':proyecto},
                                      context_instance=RequestContext(request))
    else:
        formulario = RolForm(instance=rol)
        formulario.fields["permissions"].queryset = Permission.objects.filter(content_type=12)
    return render_to_response('proyecto/rol/modificar_rol.html',
                              {'usuario_actor': usuario_actor, 'rol': rol, 'formulario': formulario, 'proyecto':proyecto},
                              context_instance=RequestContext(request))

@user_passes_test(User.puede_eliminar_roles, login_url="/iniciar_sesion")
def confirmar_eliminar_rol(request, id_proyecto, idRol):
    """

    :param request:
    :param idRol:
    :return:
    """
    usuario_actor = request.user
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    rol = Group.objects.get(pk=idRol)
    return render_to_response('proyecto/rol/conf_eliminar_rol.html', {'usuario_actor': usuario_actor, 'rol': rol, 'proyecto':proyecto},
                              context_instance=RequestContext(request))

@user_passes_test(User.puede_eliminar_roles, login_url="/iniciar_sesion")
def eliminar_rol(request, id_proyecto, idRol):
    """

    :param request:
    :param idRol:
    :return:
    """
    rol = Group.objects.get(pk=idRol)
    rol.delete()
    usuario_actor = request.user
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    roles = Group.objects.filter(Proyecto=proyecto).order_by('id')
    return render_to_response('proyecto/rol/rol_exito.html',
                              {'usuario_actor': usuario_actor, 'roles': roles,
                               'mensaje':'El rol ha sido eliminado con exito', 'proyecto':proyecto},
                              context_instance=RequestContext(request))

@user_passes_test(User.puede_modificar_usuarios, login_url="/iniciar_sesion")
def asignar_rol(request, id_proyecto, id_usuario):
    """
    :param request:
    :param idRol:
    :return:
    """
    usuario_actor = request.user
    usuario = User.objects.get(pk=id_usuario)
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    roles = list(usuario.groups.all().exclude(Proyecto=proyecto))
    lista_usuarios = proyecto.Usuarios.all().order_by('pk')

    if request.method == 'POST':
        formulario = AsignarRol(request.POST, instance=usuario)
        formulario.fields["groups"].queryset = Group.objects.filter(Proyecto=proyecto)
        if formulario.is_valid():
            formulario.save()
            for rol in roles:
                usuario.groups.add(rol)
            usuario.save()
            return render_to_response('proyecto/rol/asignar_rol_exito.html',
                                     {'mensaje': 'Rol asignado con exito', 'usuario_actor': usuario_actor,
                                      'lista_usuarios': lista_usuarios,'proyecto':proyecto}, context_instance=RequestContext(request))
    else:
        formulario = AsignarRol(instance=usuario)
        formulario.fields["groups"].queryset = Group.objects.filter(Proyecto=proyecto)
    return render(request, 'proyecto/rol/form_asignar.html', {'formulario': formulario,
                                                 'operacion': 'Seleccione el rol que desea asignar al usuario',
                                                 'usuario_actor': usuario_actor, 'usuario': usuario, 'proyecto':proyecto},
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
@user_passes_test(User.puede_consultar_atributos, login_url="/iniciar_sesion")
def administrar_atributo(request, id_proyecto, id_fase):
    """

    :param request:
    :return:
    """
    usuario_actor = request.user
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    fase = Fase.objects.get(pk=id_fase)
    lista_atributos = Atributo.objects.filter(Fase=fase)

    return render_to_response('proyecto/fase/atributo/administrar_atributo.html',
                              {'usuario_actor': usuario_actor, 'lista_atributos': lista_atributos,
                               'proyecto': proyecto, 'fase': fase},
                              context_instance=RequestContext(request))


@user_passes_test(User.puede_agregar_atributos, login_url="/iniciar_sesion")
def crear_atributo(request, id_proyecto, id_fase):
    usuario_actor = request.user
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    fase = Fase.objects.get(pk=id_fase)
    atributo = Atributo(Usuario=usuario_actor, Fase=fase)
    lista_atributos = Atributo.objects.filter(Fase=fase)
    if proyecto.Estado == 'C':
            return render_to_response('proyecto/fase/atributo/atributo_error.html',
                              {'usuario_actor': usuario_actor, 'proyecto': proyecto, 'lista_atributos': lista_atributos,
                               'mensaje': 'No puedes crear un atributo a un proyecto que ha sido cancelado', 'fase': fase},
                              context_instance=RequestContext(request))
    elif proyecto.Estado == 'F':
            return render_to_response('proyecto/fase/atributo/atributo_error.html',
                              {'usuario_actor': usuario_actor, 'proyecto': proyecto, 'lista_atributos': lista_atributos,
                               'mensaje': 'No puedes crear un atributo a un atributo de un proyecto que ha finalizado', 'fase': fase},
                              context_instance=RequestContext(request))
    elif proyecto.Estado == 'A':
            return render_to_response('proyecto/fase/atributo/atributo_error.html',
                              {'usuario_actor': usuario_actor, 'proyecto': proyecto, 'lista_atributos': lista_atributos,
                               'mensaje': 'No puedes crear un atributo a un atributo de un proyecto que ha iniciado', 'fase': fase},
                              context_instance=RequestContext(request))
    elif request.method == 'POST':
        formulario = AtributoForm(request.POST, instance=atributo)
        if formulario.is_valid():
            formulario.save()
            atributo_nombre = str(request.POST['Nombre'])
            return render_to_response('proyecto/fase/atributo/atributo_exito.html',
                                      {'mensaje': 'El atributo '+atributo_nombre+' se ha creado exitosamente',
                                       'usuario_actor': usuario_actor, 'lista_atributos':lista_atributos,
                                       'proyecto': proyecto, 'fase': fase},
                                      context_instance=RequestContext(request))
    else:
        formulario = AtributoForm(instance=atributo)
    return render_to_response('proyecto/fase/atributo/atributo_form.html',
                              {'formulario': formulario, 'operacion': 'Ingrese los datos del atributo',
                               'usuario_actor': usuario_actor, 'proyecto': proyecto, 'fase': fase},
                              context_instance=RequestContext(request))

@user_passes_test(User.puede_consultar_atributos, login_url="/iniciar_sesion")
def detalle_atributo(request, id_proyecto, id_fase, id_atributo):
    """

    :param request:
    :param idRol:
    :return:
    """
    usuario_actor = request.user
    atributo = Atributo.objects.get(pk=id_atributo)
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    fase = Fase.objects.get(pk=id_fase)
    return render_to_response('proyecto/fase/atributo/detalle_atributo.html',
                              {'usuario_actor': usuario_actor,
                               'atributo': atributo, 'proyecto': proyecto, 'fase': fase},
                              context_instance=RequestContext(request))


@user_passes_test(User.puede_modificar_atributos, login_url="/iniciar_sesion")
def modificar_atributo(request, id_proyecto, id_fase, id_atributo):
    """

    :param request:
    :param id_proyecto:
    :param id_atributo:
    :return:
    """
    usuario_actor = request.user
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    fase = Fase.objects.get(pk=id_fase)
    lista_atributos = Atributo.objects.filter(Fase=fase).order_by('id')
    atributo = Atributo.objects.get(pk=id_atributo)

    if proyecto.Estado == 'C':
            return render_to_response('proyecto/fase/atributo/atributo_error.html',
                              {'usuario_actor': usuario_actor, 'proyecto': proyecto, 'lista_atributos': lista_atributos,
                               'mensaje': 'No puedes modificar los datos un atributo de un proyecto que ha sido cancelado', 'fase': fase},
                              context_instance=RequestContext(request))
    elif proyecto.Estado == 'F':
            return render_to_response('proyecto/fase/atributo/atributo_error.html',
                              {'usuario_actor': usuario_actor, 'proyecto': proyecto, 'lista_atributos': lista_atributos,
                               'mensaje': 'No puedes modificar los datos un atributo de un proyecto que ha finalizado', 'fase': fase},
                              context_instance=RequestContext(request))
    elif proyecto.Estado == 'A':
            return render_to_response('proyecto/fase/atributo/atributo_error.html',
                              {'usuario_actor': usuario_actor, 'proyecto': proyecto, 'lista_atributos': lista_atributos,
                               'mensaje': 'No puedes modificar los datos un atributo de un proyecto que ha iniciado', 'fase': fase},
                              context_instance=RequestContext(request))
    elif request.method == 'POST':
        formulario = AtributoForm(request.POST, instance=atributo)
        if formulario.is_valid():
            formulario.save()
            return render_to_response('proyecto/fase/atributo/atributo_exito.html',
                                      {'mensaje': 'El atributo '+atributo.Nombre+' se ha modificado exitosamente',
                                       'usuario_actor': usuario_actor, 'proyecto':proyecto, 'atributo': atributo,
                                       'lista_atributos': lista_atributos, 'fase': fase},
                                      context_instance=RequestContext(request))
        else:
            return render_to_response('proyecto/fase/atributo/atributo_form.html',
                              {'formulario': formulario, 'operacion': 'Modificar atributo',
                               'usuario_actor': usuario_actor,  'proyecto': proyecto, 'atributo': atributo, 'fase': fase},
                              context_instance=RequestContext(request))
    else:
        formulario = AtributoForm(instance=atributo)
        return render_to_response('proyecto/fase/atributo/atributo_form.html',
                              {'formulario': formulario, 'operacion': 'Modificar atributo',
                               'usuario_actor': usuario_actor,  'proyecto': proyecto, 'atributo': atributo, 'fase': fase},
                              context_instance=RequestContext(request))




@user_passes_test(User.puede_eliminar_atributos, login_url="/iniciar_sesion")
def eliminar_atributo(request, id_proyecto, id_fase, id_atributo):
    """

    :param request:
    :param idRol:
    :return:
    """
    atributo = Atributo.objects.get(pk=id_atributo)
    atributo_nombre = atributo.Nombre
    atributo.delete()
    usuario_actor = request.user
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    fase = Fase.objects.get(pk=id_fase)

    lista_atributos = Atributo.objects.filter(Fase=fase).order_by('id')
    return render_to_response('proyecto/fase/atributo/atributo_exito.html',
                              {'usuario_actor': usuario_actor,'mensaje':'El atributo '+atributo_nombre+' ha sido eliminado exitosamente',
                               'lista_atributos': lista_atributos ,  'proyecto': proyecto, 'fase': fase},
                              context_instance=RequestContext(request))

@user_passes_test(User.puede_eliminar_atributos, login_url="/iniciar_sesion")
def confirmar_eliminar_atributo(request, id_proyecto, id_fase, id_atributo):
    """

    :param request:
    :param idFase:
    :param id_proyecto:
    :return:
    """

    usuario_actor = request.user
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    fase = Fase.objects.get(pk=id_fase)
    lista_atributos = Atributo.objects.filter(Fase=fase).order_by('id')

    if proyecto.Estado == 'A':
                return render_to_response('proyecto/fase/atributo/atributo_error.html',
                              {'usuario_actor': usuario_actor, 'proyecto': proyecto, 'lista_atributos': lista_atributos,
                               'mensaje': 'No puedes eliminar un atributo de un proyecto que ha iniciado', 'fase': fase},
                              context_instance=RequestContext(request))
    else:
        if proyecto.Estado == 'C':
                return render_to_response('proyecto/fase/atributo/atributo_error.html',
                              {'usuario_actor': usuario_actor, 'proyecto': proyecto, 'lista_atributos': lista_atributos,
                               'mensaje': 'No puedes eliminar un atributo de un proyecto que ha sido cancelado', 'fase': fase},
                              context_instance=RequestContext(request))
        else:
            if proyecto.Estado == 'F':
                return render_to_response('proyecto/fase/atributo/atributo_error.html',
                              {'usuario_actor': usuario_actor, 'proyecto': proyecto, 'lista_atributos': lista_atributos,
                               'mensaje': 'No puedes eliminar un atributo de un proyecto que ha finalizado', 'fase': fase},
                              context_instance=RequestContext(request))
            else:
                atributo = Atributo.objects.get(pk=id_atributo)
                return render_to_response('proyecto/fase/atributo/conf_eliminar_atributo.html',
                              {'usuario_actor': usuario_actor, 'atributo': atributo, 'proyecto': proyecto, 'fase': fase},
                              context_instance=RequestContext(request))

########################################################################################################################
########################################Vistas de tipo de item##########################################################
########################################################################################################################

@user_passes_test(User.puede_consultar_tipodeitem, login_url="/iniciar_sesion")
def administrar_tipoItem(request, id_proyecto, id_fase):
    """

    :param request:
    :param id_proyecto:
    :return:
    """
    usuario_actor = request.user
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    fase = Fase.objects.get(pk=id_fase)
    lista_tipos = TipoDeItem.objects.filter(Fase=fase)
    return render_to_response('proyecto/fase/tipoItem/administrar_tipoItem.html',
                              {'usuario_actor': usuario_actor, 'lista_tipos': lista_tipos,
                               'proyecto': proyecto, 'fase': fase},
                              context_instance=RequestContext(request))

@user_passes_test(User.puede_agregar_tipodeitem, login_url="/iniciar_sesion")
def crear_tipoItem(request, id_proyecto, id_fase):
    """

    :param request:
    :param id_proyecto:
    :return:
    """
    usuario_actor = request.user
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    fase = Fase.objects.get(pk=id_fase)
    tipo = TipoDeItem(Usuario=usuario_actor, Fase=fase)
    lista_tipos = TipoDeItem.objects.filter(Fase=fase)
    if proyecto.Estado == 'C':
            return render_to_response('proyecto/fase/tipoItem/tipoItem_error.html',
                              {'usuario_actor': usuario_actor, 'proyecto': proyecto, 'lista_tipos': lista_tipos,
                               'mensaje': 'No puedes crear un tipo de item a un proyecto que ha sido cancelado', 'fase': fase},
                              context_instance=RequestContext(request))
    elif proyecto.Estado == 'F':
            return render_to_response('proyecto/fase/tipoItem/tipoItem_error.html',
                              {'usuario_actor': usuario_actor, 'proyecto': proyecto, 'lista_tipos': lista_tipos,
                               'mensaje': 'No puedes crear un tipo de item a un proyecto que ha finalizado', 'fase': fase},
                              context_instance=RequestContext(request))
    elif proyecto.Estado == 'A':
            return render_to_response('proyecto/fase/tipoItem/tipoItem_error.html',
                              {'usuario_actor': usuario_actor, 'proyecto': proyecto, 'lista_tipos': lista_tipos,
                               'mensaje': 'No puedes crear un tipo de item a un proyecto que ha finalizado', 'fase': fase},
                              context_instance=RequestContext(request))
    elif Atributo.objects.filter(Fase=fase).exists() != True:
        return render_to_response('proyecto/fase/tipoItem/tipoItem_error.html',
                                      {'mensaje': 'Aun no existen atributos en esta fase, por favor creelos para continuar',
                                       'usuario_actor': usuario_actor, 'lista_tipos': lista_tipos,
                                       'proyecto': proyecto, 'fase': fase}, context_instance=RequestContext(request))
    elif request.method == 'POST':
        formulario = tipoItemForm(request.POST, instance=tipo)
        formulario.fields["Atributos"].queryset = Atributo.objects.filter(Fase=fase)
        formulario.fields["Atributos"].help_text = "Haga doble click en el Atributo que desee agregar"
        if formulario.is_valid():
            formulario.save()
            tipo_nombre = str(request.POST['Nombre'])
            return render_to_response('proyecto/fase/tipoItem/tipoItem_exito.html',
                                  {'mensaje': 'El tipo de item '+tipo_nombre+' se ha creado exitosamente',
                                   'usuario_actor': usuario_actor, 'lista_tipos': lista_tipos,
                                   'proyecto': proyecto, 'fase': fase}, context_instance=RequestContext(request))
    else:
        formulario = tipoItemForm(instance=tipo)
        formulario.fields["Atributos"].queryset = Atributo.objects.filter(Fase=fase)
        formulario.fields["Atributos"].help_text = "Haga doble click en el Atributo que desee agregar"
    return render_to_response('proyecto/fase/tipoItem/tipoItem_form.html',
                          {'formulario': formulario, 'operacion': 'Ingrese los datos del tipo de item',
                           'usuario_actor': usuario_actor, 'proyecto': proyecto, 'fase': fase},
                          context_instance=RequestContext(request))

@user_passes_test(User.puede_consultar_tipodeitem, login_url="/iniciar_sesion")
def detalle_tipoItem(request, id_proyecto, id_fase, id_tipo):
    """
    :param request:
    :param id_tipo:
    :param id_proyecto:
    :return:
    """
    usuario_actor = request.user
    tipo = TipoDeItem.objects.get(pk=id_tipo)
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    fase = Fase.objects.get(pk=id_fase)
    return render_to_response('proyecto/fase/tipoItem/detalle_tipoItem.html',
                              {'usuario_actor': usuario_actor,
                               'tipo': tipo, 'proyecto': proyecto, 'fase': fase},
                              context_instance=RequestContext(request))

@user_passes_test(User.puede_modificar_tipodeitem, login_url="/iniciar_sesion")
def modificar_tipo(request, id_proyecto, id_fase, id_tipo ):
    """

    :param request:
    :param id_proyecto:
    :param id_tipo:
    :return:
    """
    usuario_actor = request.user
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    fase = Fase.objects.get(pk=id_fase)
    lista_tipos = TipoDeItem.objects.filter(Fase=fase).order_by('id')
    tipo = TipoDeItem.objects.get(pk=id_tipo)

    if proyecto.Estado == 'C':
            return render_to_response('proyecto/fase/tipoItem/tipoItem_error.html',
                              {'usuario_actor': usuario_actor, 'proyecto': proyecto, 'lista_tipos': lista_tipos,
                               'mensaje': 'No puedes modificar los datos un tipo de item de un proyecto que ha sido cancelado', 'fase': fase},
                              context_instance=RequestContext(request))
    elif proyecto.Estado == 'F':
            return render_to_response('proyecto/fase/tipoItem/tipoItem_error.html',
                              {'usuario_actor': usuario_actor, 'proyecto': proyecto, 'lista_tipos': lista_tipos,
                               'mensaje': 'No puedes modificar los datos un tipo de item de un proyecto que ha finalizado', 'fase': fase},
                              context_instance=RequestContext(request))
    elif proyecto.Estado == 'A':
            return render_to_response('proyecto/fase/tipoItem/tipoItem_error.html',
                              {'usuario_actor': usuario_actor, 'proyecto': proyecto, 'lista_tipos': lista_tipos,
                               'mensaje': 'No puedes modificar los datos un tipo de item de un proyecto que ha iniciado', 'fase': fase},
                              context_instance=RequestContext(request))
    elif request.method == 'POST':
        formulario = tipoItemForm(request.POST, instance=tipo)
        formulario.fields["Atributos"].queryset = Atributo.objects.filter(Fase=fase)
        formulario.fields["Atributos"].help_text = "Haga doble click en el Atributo que desee agregar"
        if formulario.is_valid():
            formulario.save()
            return render_to_response('proyecto/fase/tipoItem/tipoItem_exito.html',
                                      {'mensaje': 'El tipo de item '+tipo.Nombre+' se ha modificado exitosamente',
                                       'usuario_actor': usuario_actor, 'proyecto':proyecto, 'tipo':tipo,
                                       'lista_tipos': lista_tipos, 'fase': fase},
                                      context_instance=RequestContext(request))
        else:
            return render_to_response('proyecto/fase/tipoItem/tipoItem_form.html',
                              {'formulario': formulario, 'operacion': 'Modificar tipo de item',
                               'usuario_actor': usuario_actor,  'proyecto':proyecto, 'tipo': tipo, 'fase': fase},
                              context_instance=RequestContext(request))
    else:
        formulario = tipoItemForm(instance=tipo)
        formulario.fields["Atributos"].queryset = Atributo.objects.filter(Fase=fase)
        formulario.fields["Atributos"].help_text = "Haga doble click en el Atributo que desee agregar"
    return render_to_response('proyecto/fase/tipoItem/tipoItem_form.html',
                              {'formulario': formulario, 'operacion': 'Modificar tipo de item',
                               'usuario_actor': usuario_actor,  'proyecto':proyecto, 'tipo': tipo, 'fase': fase},
                              context_instance=RequestContext(request))

@user_passes_test(User.puede_eliminar_tipodeitem, login_url="/iniciar_sesion")
def eliminar_tipo(request, id_proyecto, id_fase, id_tipo):
    """

    :param request:
    :param id_tipo:
    :param id_proyecto:
    :return:
    """
    tipo = TipoDeItem.objects.get(pk=id_tipo)
    tipo_nombre = tipo.Nombre
    tipo.delete()
    usuario_actor = request.user
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    fase = Fase.objects.get(pk=id_fase)
    lista_tipos = TipoDeItem.objects.filter(Fase=fase).order_by('id')
    return render_to_response('proyecto/fase/tipoItem/tipoItem_exito.html',
                              {'usuario_actor': usuario_actor,'mensaje':'El tipo de item '+tipo_nombre+' ha sido eliminado exitosamente',
                               'lista_tipos': lista_tipos, 'proyecto': proyecto, 'fase': fase},
                              context_instance=RequestContext(request))

@user_passes_test(User.puede_eliminar_tipodeitem, login_url="/iniciar_sesion")
def confirmar_eliminar_tipo(request, id_proyecto, id_fase, id_tipo):
    """

    :param request:
    :param idFase:
    :param id_proyecto:
    :return:
    """

    usuario_actor = request.user
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    fase = Fase.objects.get(pk=id_fase)
    lista_tipos = TipoDeItem.objects.filter(Fase=fase).order_by('id')
    if proyecto.Estado == 'A':
            return render_to_response('proyecto/fase/tipoItem/tipoItem_error.html',
                              {'usuario_actor': usuario_actor, 'proyecto': proyecto, 'lista_tipos': lista_tipos,
                               'mensaje': 'No puedes eliminar un tipo de item de un proyecto que ha iniciado', 'fase': fase},
                              context_instance=RequestContext(request))
    elif proyecto.Estado == 'C':
            return render_to_response('proyecto/fase/tipoItem/tipoItem_error.html',
                              {'usuario_actor': usuario_actor, 'proyecto': proyecto, 'lista_tipos': lista_tipos,
                               'mensaje': 'No puedes eliminar un tipo de item de un proyecto que ha sido cancelado', 'fase': fase},
                              context_instance=RequestContext(request))
    elif proyecto.Estado == 'F':
            return render_to_response('proyecto/fase/tipoItem/tipoItem_error.html',
                              {'usuario_actor': usuario_actor, 'proyecto': proyecto, 'lista_tipos': lista_tipos,
                               'mensaje': 'No puedes eliminar un tipo de item de un proyecto que ha finalizado', 'fase': fase},
                              context_instance=RequestContext(request))
    else:
            tipo = TipoDeItem.objects.get(pk=id_tipo)
            return render_to_response('proyecto/fase/tipoItem/conf_eliminar_tipo.html',
                              {'usuario_actor': usuario_actor, 'tipo': tipo, 'proyecto': proyecto, 'fase': fase},
                              context_instance=RequestContext(request))

@user_passes_test(User.puede_agregar_tipodeitem, login_url="/iniciar_sesion")
def importar_tipo(request, id_proyecto, id_fase):
    usuario_actor = request.user
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    fase = Fase.objects.get(pk=id_fase)
    lista_tipos = TipoDeItem.objects.filter(Fase=fase)
    if request.method == 'POST':
        formulario = tipoItemImportar(request.POST)
        formulario.fields["tipos"].queryset = TipoDeItem.objects.exclude(Fase=fase)
        formulario.fields["tipos"].help_text = "Haga doble click en el Tipo de item que desee agregar"
        mensaje = ''
        if formulario.is_valid():
            importados = formulario.cleaned_data['tipos']
            for importado in importados:
                tipo = TipoDeItem.objects.create(Nombre=importado.Nombre, Usuario=usuario_actor, Fase=fase)
                tipo.Atributos = importado.Atributos.all()
                mensaje += 'Se ha importado exitosamente el tipo de item '+tipo.Nombre+' de la fase '+importado.Fase.Nombre +' del proyecto '+importado.Fase.Proyecto.Nombre +'\n'
                tipo.save()

            return render_to_response('proyecto/fase/tipoItem/tipoItem_exito.html',
                                      {'mensaje': mensaje,
                                       'usuario_actor': usuario_actor, 'lista_tipos': lista_tipos,
                                       'proyecto': proyecto, 'fase': fase}, context_instance=RequestContext(request))
    else:
        formulario = tipoItemImportar()
        formulario.fields["tipos"].queryset = TipoDeItem.objects.exclude(Fase=fase)
        formulario.fields["tipos"].help_text = "Haga doble click en el Tipo de item que desee agregar"
    return render_to_response('proyecto/fase/tipoItem/tipoItem_form.html',
                              {'formulario': formulario, 'operacion': 'Seleccione los tipos de items que desea importar',
                               'usuario_actor': usuario_actor, 'proyecto': proyecto, 'fase': fase},
                              context_instance=RequestContext(request))
