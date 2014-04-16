from django.shortcuts import render_to_response,render,HttpResponseRedirect,HttpResponse, RequestContext
from administracion.models import Fase
from administracion.forms import FaseForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User



# Create your views here.
def lista_usuarios(request):
    usuarios = User.objects.all()
    return render_to_response('lista_usuario.html', {'usuarios':usuarios})

def nuevo_usuario(request):
    if request.method == 'POST':
        formulario = UserCreationForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return render_to_response('administracionmensaje.html', context_instance=RequestContext(request))
    else:
        formulario = UserCreationForm()
    return render_to_response('usuarioform.html', {'formulario': formulario}, context_instance=RequestContext(request))


def ingresar(request):
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
                    return render_to_response('noactivo.html', context_instance=RequestContext(request))
            else:
                return render_to_response('ingresarerror.html', context_instance=RequestContext(request))
    else:
        formulario = AuthenticationForm()
    return render_to_response('ingresar.html', {'formulario': formulario}, context_instance=RequestContext(request))

@login_required(login_url='/ingresar')
def privado(request):
    usuario = request.user
    return render_to_response('privado.html', {'usuario':usuario}, context_instance=RequestContext(request))

@login_required(login_url='/ingresar')
def cerrar(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required(login_url='/ingresar')
def administracion(request):
    usuario = request.user.get_full_name()
    return render_to_response('administracion.html', {'usuario':usuario}, context_instance=RequestContext(request))

@login_required(login_url='/ingresar')
def admfases(request):
    usuario = request.user.get_full_name()
    fases = Fase.objects.all()
    return render_to_response('adm-fases.html', {'usuario':usuario, 'fases':fases}, context_instance=RequestContext(request))

@login_required(login_url='/ingresar')
def crearfase(request):
    usuario = request.user.get_full_name()
    if request.method=='POST':
        formulario = FaseForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/admfases')
    else:
        formulario = FaseForm()
    return render_to_response('creacion-fase.html', {'usuario':usuario, 'formulario':formulario}, context_instance=RequestContext(request))
