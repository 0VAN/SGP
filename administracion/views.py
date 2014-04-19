from django.shortcuts import render_to_response, render, HttpResponseRedirect, HttpResponse, RequestContext, get_object_or_404
from administracion.forms import UsuarioForm, ProyectoForm, UsuarioModForm, UsuarioDelForm, FaseForm, RolForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group, Permission
from administracion.models import Proyecto, Fase

# Create your views here.

########################################################################################################################

"""
    Vista de inicio de sesion
"""
def iniciar_sesion(request):
    if not request.user.is_anonymous():
        return administracion(request)
    if request.method == 'POST':
        formulario = AuthenticationForm(request.POST)
        if formulario.is_valid:
            usuario = request.POST['username']
            clave = request.POST['password']
            acceso = authenticate(username=usuario, password=clave)
            if acceso is not None:
                if acceso.is_active:
                    login(request, acceso)
                    return administracion(request)
                else:
                    return render_to_response('no_activo.html', context_instance=RequestContext(request))
            else:
                return render_to_response('sesion_error.html', context_instance=RequestContext(request))
    else:
        formulario = AuthenticationForm()
    return render_to_response('iniciar_sesion.html', {'formulario': formulario},
                              context_instance=RequestContext(request))


"""
    Vista que muestra el contenido privado del modulo de administracion
"""
@login_required(login_url='/iniciar_sesion')
def privado(request):
    usuario = request.user
    return render_to_response('privado_administrador.html', {'usuario':usuario},
                              context_instance=RequestContext(request))


"""
    Vista para cerrar la sesion de un ususario
"""
@login_required(login_url='/iniciar_sesion')
def cerrar_sesion(request):
    logout(request)
    return HttpResponseRedirect('/')


"""
    Vista que muestra el contenido privado del modulo de administracion
"""
@login_required(login_url='/iniciar_sesion')
def administracion(request):
    usuarios = User.objects.all()
    usuario = request.user
    return render_to_response('administracion.html', {'lista_usuarios': usuarios, 'usuario':usuario},
                              context_instance=RequestContext(request))

#############################################Vistas de Administracion de Usuarios#######################################

"""
    Vista de administrar usuario
"""
@user_passes_test( User.can_administrar_usuario , login_url="/iniciar_sesion")
def administrar_usuario(request):
    usuario = request.user
    return render_to_response('usuario/administrar_usuario.html', {'usuario':usuario},
                              context_instance=RequestContext(request))
"""
    Vista de creacion de nuevo usuario
"""
@user_passes_test( User.can_add_user , login_url="/iniciar_sesion")
def crear_usuario(request):
    if request.method == 'POST':
        formulario = UsuarioForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return render_to_response('usuario/operacion_usuario_exito.html', {'mensaje': 'Usuario creado con exito'}
                                      , context_instance=RequestContext(request))
    else:
        formulario = UsuarioForm()
    return render_to_response('usuario/form_usuario.html',
                              {'formulario': formulario, 'mensaje': 'Creacion de un nuevo usuario'},
                              context_instance=RequestContext(request))
"""
    Vista de modificacion de nuevo usuario
"""
@user_passes_test( User.can_change_user , login_url="/iniciar_sesion")
def modificar_usuario(request):
    usuario = request.user
    if request.method == 'POST':
        formulario = UsuarioModForm(request.POST, instance=usuario)
        if formulario.is_valid():
           form = formulario.save(commit=False)
           form.user = request
           form.save()
           return render_to_response('usuario/operacion_usuario_exito.html',
                                     {'mensaje': 'Usuario modificado con exito'},
                                     context_instance=RequestContext(request))
    else:
        formulario = UsuarioModForm(instance=usuario)
    return render(request, 'usuario/form_usuario.html',
                  {'usuario': usuario, 'formulario': formulario, 'mensaje': 'Modificacion del usuario'},
                  context_instance=RequestContext(request))

@user_passes_test( User.can_change_user , login_url="/iniciar_sesion")
def cambioEstado_usuario(request):
    usuarios = User.objects.all()
    return render_to_response('usuario/cambioEstado_usuario.html', {'lista_usuarios': usuarios,'usuarioActor':request.user},
                              context_instance=RequestContext(request))

@user_passes_test( User.can_change_user , login_url="/iniciar_sesion")
def cambioEstado_usuario_form(request, id_usuario):
    usuario = User.objects.get(pk=id_usuario)
    if request.method == 'POST':
        formulario = UsuarioDelForm(request.POST, instance=usuario)
        if formulario.is_valid():
           form = formulario.save(commit=False)
           form.user = request
           form.save()
           return render_to_response('usuario/operacion_usuario_exito.html',
                                     {'mensaje':'Cambio de estado de usuario con exito'}
                                     , context_instance=RequestContext(request))
    else:
        formulario = UsuarioDelForm(instance=usuario)
    return render(request, 'usuario/form_usuario.html',
                  {'usuario': usuario, 'formulario': formulario, 'mensaje': 'Cambio de estado del usuario'},
                  context_instance=RequestContext(request))

@user_passes_test( User.can_administrar_usuario , login_url="/iniciar_sesion")
def detalle_usuario(request, id_usuario):
    usuario = get_object_or_404(User, pk=id_usuario)
    return render_to_response('usuario/detalle_usuario.html', {'usuario': usuario},
                              context_instance=RequestContext(request))

###########################################Vistas de Administrar Proyecto###############################################

@user_passes_test( User.can_administrar_proyecto , login_url="/iniciar_sesion")
def administrar_proyecto(request):
    lista_proyectos = Proyecto.objects.all()
    usuario = request.user
    return render_to_response('proyecto/administrar_proyecto.html',
                              {'lista_proyecto': lista_proyectos, 'usuario':usuario}, context_instance=RequestContext(request))

@user_passes_test( User.can_add_proyecto , login_url="/iniciar_sesion")
def nuevo_proyecto(request):
      if request.method == 'POST':
        formulario = ProyectoForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return render_to_response('proyecto/crear_proyecto_exito.html', context_instance=RequestContext(request))
      else:
        formulario = ProyectoForm()
      return render_to_response('proyecto/crear_proyecto.html', {'formulario': formulario},
                                context_instance=RequestContext(request))

###########################################Vistas de administracion de Fase#############################################

@user_passes_test( User.can_administrar_fase , login_url="/iniciar_sesion")
def administrar_fases(request):
    usuario = request.user.get_full_name()
    fases = Fase.objects.all()
    return render_to_response('proyecto/fase/adm-fases.html', {'usuario':usuario, 'fases':fases}, context_instance=RequestContext(request))

@user_passes_test( User.can_add_fase , login_url="/iniciar_sesion")
def crear_fase(request):
    usuario = request.user.get_full_name()
    fase = Fase(Usuario= request.user)
    if request.method=='POST':
        formulario = FaseForm(request.POST, instance=fase)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/administracion/proyectos/fases')
    else:
        formulario = FaseForm()
    return render_to_response('proyecto/fase/creacion-fase.html', {'usuario':usuario, 'formulario':formulario}, context_instance=RequestContext(request))

@user_passes_test( User.can_administrar_fase , login_url="/iniciar_sesion")
def detalle_fase(request, idFase):
    usuario = request.user.get_full_name()
    fase = Fase.objects.get(pk=idFase)
    return render_to_response('proyecto/fase/detallefase.html', {'usuario':usuario, 'fase':fase}, context_instance=RequestContext(request))

@user_passes_test( User.can_change_fase , login_url="/iniciar_sesion")
def modificar_fase(request, idFase):
    usuario = request.user.get_full_name()
    fase = Fase.objects.get(pk=idFase)
    formulario = FaseForm(request.POST, instance=fase)
    if formulario.is_valid():
        formulario.save()
        return HttpResponseRedirect('/administracion/proyectos/fases/')
    else:
        formulario = FaseForm(instance=fase)
    return render_to_response('proyecto/fase/mod-fase.html', {'usuario':usuario, 'formulario':formulario}, context_instance=RequestContext(request))

@user_passes_test( User.can_delete_fase , login_url="/iniciar_sesion")
def vista_eliminar_fase(request, idFase):
    usuario = request.user.get_full_name()
    fase = Fase.objects.get(pk=idFase)
    return render_to_response('proyecto/fase/eliminarfase.html', {'usuario':usuario, 'fase':fase}, context_instance=RequestContext(request))

@user_passes_test( User.can_delete_fase , login_url="/iniciar_sesion")
def eliminar_fase(request, idFase):
    fase = Fase.objects.get(pk=idFase)
    fase.delete()
    return render_to_response('proyecto/fase/faseeliminada.html')

###########################################Vistas de administracion de Rol##############################################

@user_passes_test( User.can_administrar_rol , login_url="/iniciar_sesion")
def administrar_roles(request):
    usuario = request.user
    roles = Group.objects.all()
    return render_to_response('rol/administrar_rol.html', {'usuario':usuario, 'roles':roles}, context_instance=RequestContext(request))

@user_passes_test( User.can_add_group , login_url="/iniciar_sesion")
def crear_rol(request):
    mensaje="Rol creado con exito"
    if request.method == 'POST':
        formulario = RolForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return render_to_response('rol/crear_rol_exito.html', {'mensaje':mensaje},context_instance=RequestContext(request))
    else:
        formulario = RolForm()
    return render_to_response('rol/crear_rol.html', {'formulario':formulario},context_instance=RequestContext(request))

@user_passes_test( User.can_administrar_rol , login_url="/iniciar_sesion")
def detalle_rol(request, idRol):
    usuario = request.user.get_full_name()
    rol = Group.objects.get(pk=idRol)
    return render_to_response('rol/detallerol.html', {'usuario':usuario, 'rol':rol}, context_instance=RequestContext(request))

@user_passes_test( User.can_change_group , login_url="/iniciar_sesion")
def modificar_rol(request, idRol):
    usuario = request.user.get_full_name()
    rol = Group.objects.get(pk=idRol)
    formulario = RolForm(request.POST, instance=rol)
    if formulario.is_valid():
        formulario.save()
        return HttpResponseRedirect('/administracion/roles/')
    else:
        formulario = RolForm(instance=rol)
    return render_to_response('rol/modificar_rol.html', {'usuario':usuario, 'formulario':formulario}, context_instance=RequestContext(request))

@user_passes_test( User.can_delete_group , login_url="/iniciar_sesion")
def vista_eliminar_rol(request, idRol):
    usuario = request.user.get_full_name()
    rol = Group.objects.get(pk=idRol)
    return render_to_response('rol/eliminarrol.html', {'usuario':usuario, 'rol':rol}, context_instance=RequestContext(request))

@user_passes_test( User.can_delete_group , login_url="/iniciar_sesion")
def eliminar_rol(request, idRol):
    rol = Group.objects.get(pk=idRol)
    rol.delete()
    return render_to_response('rol/roleliminado.html',context_instance=RequestContext(request))
