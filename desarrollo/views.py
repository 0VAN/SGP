from django.shortcuts import render_to_response, render, HttpResponseRedirect, HttpResponse, RequestContext, get_object_or_404
from administracion.forms import ProyectoForm, UsuarioModForm, UsuarioDelForm, FaseForm, RolForm, AsignarRol
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group, Permission
from administracion.models import Proyecto, Fase, TipoDeItem
from desarrollo.models import *
from desarrollo.forms import *

@login_required(login_url='/iniciar_sesion')
def desarrollo(request):
    """

    :param request:
    :return:

    Vista que muestra el contenido privado del modulo de desarrollo

    | Recibe como parametro un request y retorna la pagina web desarrollo.html donde se muestra la
    | lista de proyectos del sistema si el usuario posee los permisos correspondientes

    * Variables
        -   lista_proyectos: es la lista de proyectos existentes en el sistema
        -   usuario: es el usuario logueado
    """
    lista_proyectos = Proyecto.objects.all()
    usuario = request.user
    return render_to_response('desarrollo.html', {'lista_proyectos': lista_proyectos, 'usuario': usuario},
                              context_instance=RequestContext(request))


def des_proyecto(request, id_proyecto):
    usuario = request.user
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    lista_fases = Fase.objects.filter(Proyecto=id_proyecto)
    return render_to_response('proyecto/des_proyecto.html',
        {'usuario': usuario, 'proyecto': proyecto, 'lista_fases': lista_fases},
        context_instance=RequestContext(request))

def des_fase(request, id_proyecto, id_fase):
    usuario = request.user
    fase = Fase.objects.get(pk=id_fase)
    lista_items = Item.objects.filter(Fase=fase)
    return render_to_response('proyecto/fase/des_fase.html',
        {'usuario': usuario, 'fase': fase, 'lista_items': lista_items},
        context_instance=RequestContext(request))


def crear_item(request, id_proyecto, id_fase):
    usuario = request.user
    fase = Fase.objects.get(pk=id_fase)
    item = Item(Usuario=usuario, Fase=fase, Version=1)
    lista_tipos = TipoDeItem.objects.filter(Proyecto=fase.Proyecto)
    if request.method=='POST':
        formulario = ItemForm(request.POST, instance=item)
        if formulario.is_valid():
            formulario.save()
            item2 = Item.objects.last()
            for atributo in item2.Tipo.Atributos.all():
                campo = Campo.objects.create(item=item2, tipoItem=item2.Tipo, atributo=atributo)
                campo.save()
            return HttpResponseRedirect('/desarrollo/proyecto/'+id_proyecto+'/fase/'+id_fase)
    else:
        formulario = ItemForm()
    return render_to_response('proyecto/fase/item/crear_item.html',
        {'usuario': usuario, 'formulario': formulario, 'fase': fase, 'lista_tipos':lista_tipos},
        context_instance=RequestContext(request))

def mod_item(request, id_proyecto, id_fase, id_item):
    usuario = request.user
    fase = Fase.objects.get(pk=id_fase)
    item = Item.objects.get(pk=id_item)
    item.Version+=1
    formulario = ItemForm(request.POST, instance=item)
    lista_tipos = TipoDeItem.objects.filter(Proyecto=fase.Proyecto)
    if formulario.is_valid():
        formulario.save()
        return HttpResponseRedirect('/desarrollo/proyecto/'+id_proyecto+'/fase/'+id_fase+'/')
    else:
        formulario = ItemForm(instance=item)
    return render_to_response(
        'proyecto/fase/item/mod_item.html',
        {'usuario':usuario, 'item':item, 'fase':fase, 'formulario':formulario, 'lista_tipos': lista_tipos},
        context_instance=RequestContext(request)
    )


def completar_item(request, id_proyecto, id_fase, id_item):
    usuario = request.user
    fase = Fase.objects.get(pk=id_fase)
    item = Item.objects.get(pk=id_item)
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    campos = Campo.objects.filter(item=item)
    if request.method == 'POST':
        for a in campos:
            for key, value in request.POST.iteritems():
                if a.atributo.Nombre == key:
                    if a.atributo.Tipo == Atributo.NUMERICO:
                        a.numerico = value
                        a.save()
                    elif a.atributo.Tipo == Atributo.CADENA:
                        a.cadena = value
                        a.save()
                    elif a.atributo.Tipo == Atributo.FECHA:
                        a.fecha = value
                        a.save()
                    elif a.atributo.Tipo == Atributo.TEXTO:
                        a.texto = value
                        a.save()
                    elif a.atributo.Tipo == Atributo.LOGICO:
                        if value=="1":
                            a.logico = None
                        elif value=="2":
                            a.logico = True
                        elif value=="3":
                            a.logico = False
                        a.save()
                    elif a.atributo.Tipo == Atributo.MAIL:
                        a.mail = value
                        a.save()
                    elif a.atributo.Tipo == Atributo.HORA:
                        a.hora = value
                        a.save()
        return HttpResponseRedirect('/desarrollo/proyecto/'+id_proyecto+'/fase/'+id_fase+'/')
    #else:
    return render_to_response(
        'proyecto/fase/item/com_item.html',
        {'usuario':usuario, 'item':item, 'fase':fase, 'campos':campos},
        context_instance=RequestContext(request)
    )


def form_vista(request):
    usuario = request.user
    if request.method=='POST':
        formulario = LogicoForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            logico = Logico1.objects.last()
            return HttpResponseRedirect('/')
    else:
        formulario = LogicoForm()
    return render_to_response('form.html',
        {'usuario': usuario, 'formulario': formulario},
        context_instance=RequestContext(request))