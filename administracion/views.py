from django.shortcuts import render_to_response,render,HttpResponseRedirect,HttpResponse, RequestContext
from administracion.models import Usuario
from administracion.forms import UsuarioForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required




# Create your views here.
def lista_usuarios(request):
    usuarios = Usuario.objects.all()
    return render_to_response('lista_usuario.html', {'usuarios':usuarios})

def nuevo_usuario(request):
    if request.method == 'POST':
        formulario = UserCreationForm(request.POST)
        if formulario.is_valid:
            formulario.save()
            return HttpResponseRedirect('/')#colocar a donde se desea redireccionar
    else:
        formulario = UserCreationForm()
    return render_to_response('usuarioform.html', {'formulario': formulario}, context_instance=RequestContext(request))


def ingresar(request):
    if not request.user.is_anonymous():
        return HttpResponseRedirect('/privado')
    if request.method == 'POST':
        formulario = AuthenticationForm(request.POST)
        if formulario.is_valid:
            usuario = request.POST['username']
            clave = request.POST['password']
            acceso = authenticate(username=usuario, password=clave)
            if acceso is not None:
                if acceso.is_active:
                    login(request, acceso)
                    return HttpResponseRedirect('/privado')
                else:
                    return render_to_response('noactivo.html', context_instance=RequestContext(request))
            else:
                return render_to_response('nousuario.html', context_instance=RequestContext(request))
    else:
        formulario = AuthenticationForm()
    return render_to_response('ingresar.html', {'formulario': formulario}, context_instance=RequestContext(request))

@login_required(login_url='/ingresar')
def privado(request):
    usuario = request.user
    return render_to_response('privado.html', {'usuario':usuario}, context_instance=RequestContext(request))

@login_required(login_url='ingreso')
def cerrar(request):
    logout(request)
    return HttpResponseRedirect('/')