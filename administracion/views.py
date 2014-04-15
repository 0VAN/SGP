from django.shortcuts import render_to_response, render, HttpResponseRedirect, HttpResponse, RequestContext
from administracion.forms import UsuarioForm, ProyectoForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from administracion.models import Proyecto



# Create your views here.
"""
    Vista que lista los nuevo usuarios
"""
def lista_usuarios(request):
    usuarios = User.objects.all()
    return render_to_response('administracion.html', {'lista_usuarios': usuarios},
                              context_instance=RequestContext(request))

"""
    Vista de creacion de nuevo usuario
"""
def nuevo_usuario(request):
    if request.method == 'POST':
        formulario = UsuarioForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return render_to_response('crear_usuario_exito.html', context_instance=RequestContext(request))
    else:
        formulario = UsuarioForm()
    return render_to_response('crear_usuario.html', {'formulario': formulario},
                              context_instance=RequestContext(request))

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
    return lista_usuarios(request)

def nuevo_proyecto(request):
      if request.method == 'POST':
        formulario = ProyectoForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return render_to_response('crear_proyecto_exito.html', context_instance=RequestContext(request))
      else:
        formulario = ProyectoForm()
      return render_to_response('crear_proyecto.html', {'formulario': formulario},
                                context_instance=RequestContext(request))

def lista_proyectos(request):
    proyectos = Proyecto.objects.all()
    return render_to_response('listar_proyectos.html', {'lista_usuarios': proyectos},
                              context_instance=RequestContext(request))

def actualiza_usuario(request, id_usuario):
    usuarios = User.objects.get(pk=id_usuario)
    usuario = request.user
    if request.method == 'POST':
        formulario = UsuarioForm(request.POST, instance=usuarios)
        if formulario.is_valid():
           form = formulario.save(commit=False)
           form.firts_name = request.user
           form.save()
           return render_to_response('crear_usuario_exito.html', context_instance=RequestContext(request))
    else:
        formulario = UsuarioForm(instance=usuarios)
    return render(request, 'modificar_usuario.html', locals(), context_instance=RequestContext(request))