# -*- encoding: utf-8 -*-

from django.shortcuts import render_to_response, render, HttpResponseRedirect, HttpResponse, RequestContext, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from sesion.forms import UsuarioGestionForm
from administracion.views import administracion
from desarrollo.views import desarrollo
from gestion.views import gestion

# Create your views here.
def iniciar_sesion(request):
    """
    .. method:: Vista de inicio de sesion

        :param request:
        :return: iniciar_sesion.html

        | Recibe como parametro un request y retorna diferentes paginas web segun el estado del usuario y
        | su existencia en el sistema.

        * Si el usuario inicia sesion con exito, retorna iniciar_sesion.html
        * Si el usuario esta inactivo, retorna no_activo.html
        * Si el usuario no exite en el sistema, retorna sesion_error.html

        * Variables
            -   formulario: es el formulario que el usuario debe completar para iniciar sesion
            -   usuario_actor: es el usuario que realiza la accion
            -   clave: es la clave secreta introducida por el usuario_actor
            -   acceso: contiene el resultado de la funcion authenticate que lleva como parametro
                el par(usuario, contrasenha) verificando su existencia y estado en el sistema
    """
    if not request.user.is_anonymous():
        if request.user.esDesarrollador():
            return desarrollo(request)
        elif request.user.esLider():
            return gestion(request)
        elif request.user.esAdministrador():
            return administracion(request)
    if request.method == 'POST':
        formulario = AuthenticationForm(request.POST)
        if formulario.is_valid:
            usuario_actor = request.POST['username']
            clave = request.POST['password']
            acceso = authenticate(username=usuario_actor, password=clave)
            if acceso is not None:
                if acceso.is_active:
                    login(request, acceso)
                    if request.user.esDesarrollador():
                        return desarrollo(request)
                    elif request.user.esLider():
                        return gestion(request)
                    elif request.user.esAdministrador():
                        return administracion(request)
                else:
                    return render_to_response('no_activo.html', context_instance=RequestContext(request))
            else:
                return render_to_response('sesion_error.html', context_instance=RequestContext(request))
    else:
        formulario = AuthenticationForm()
    return render_to_response('iniciar_sesion.html', {'formulario': formulario},
                              context_instance=RequestContext(request))
@login_required(login_url='/iniciar_sesion')
def cerrar_sesion(request):
    """

    :param request:
    :return:

    Vista para cerrar la sesion de un ususario

    | Recibe como parametro un request y llama a la funcion logout con tal parametro, redirigiendo al
    | usuario a la pagina web '/' (raiz) donde se solicita el inicio de sesion de un usuario
    """
    logout(request)
    return HttpResponseRedirect('/')

@login_required(login_url="/iniciar_sesion")
def gestion_usuario(request):
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
    usuario_actor = request.user
    lista_usuarios = User.objects.all()
    if request.method == 'POST':
        formulario = UsuarioGestionForm(request.POST, instance=usuario_actor)
        if formulario.is_valid():
           formulario.save()
           return render_to_response('gestion_exito.html',
                                     {'mensaje': 'Usted ha actualizado tu informacion personal exitosamente', 'usuario_actor': usuario_actor,
                                      'lista_usuarios': lista_usuarios}, context_instance=RequestContext(request))
    else:
        formulario = UsuarioGestionForm(instance=usuario_actor)
    return render(request, 'gestion_usuario.html',
                  {'usuario_actor': usuario_actor, 'formulario': formulario, 'operacion': 'Gestion de datos personales'},
                  context_instance=RequestContext(request))