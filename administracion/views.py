from django.shortcuts import render_to_response, render, HttpResponseRedirect, HttpResponse, RequestContext
from administracion.forms import UsuarioForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User



# Create your views here.
def lista_usuarios(request):
    usuarios = User.objects.all()
    return render_to_response('administracion.html', {'lista_usuarios': usuarios}, context_instance=RequestContext(request))

def nuevo_usuario(request):
    if request.method == 'POST':
        formulario = UsuarioForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return render_to_response('crear_usuario_exito.html', context_instance=RequestContext(request))
    else:
        formulario = UsuarioForm()
    return render_to_response('usuario_form.html', {'formulario': formulario}, context_instance=RequestContext(request))


def iniciar_sesion(request):
    if not request.user.is_anonymous():
        return HttpResponseRedirect('/administracion')
    if request.method == 'POST':
        formulario = AuthenticationForm(request.POST)
        if formulario.is_valid:
            usuario = request.POST['username']
            clave = request.POST['password']
            acceso = authenticate(username=usuario, password=clave)
            if acceso is not None:
                if acceso.is_active:
                    login(request, acceso)
                    return HttpResponseRedirect('/administracion')
                else:
                    return render_to_response('no_activo.html', context_instance=RequestContext(request))
            else:
                return render_to_response('sesion_error.html', context_instance=RequestContext(request))
    else:
        formulario = AuthenticationForm()
    return render_to_response('iniciar_sesion.html', {'formulario': formulario}, context_instance=RequestContext(request))

@login_required(login_url='/iniciar_sesion')
def privado(request):
    usuario = request.user
    return render_to_response('privado_administrador.html', {'usuario':usuario}, context_instance=RequestContext(request))

@login_required(login_url='/iniciar_sesion')
def cerrar_sesion(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required(login_url='/iniciar_sesion')
def administracion(request):
    return lista_usuarios(request)