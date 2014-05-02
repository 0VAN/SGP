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
            campos(item2)
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
    formularios = []
    atributos = item.Campos.all()
    if request.method == 'POST':
        formularios = []
        for campo in atributos:
            print campo
            print campo.Tipo
            if campo.Tipo == 'N':
                formularios.append(NumericoForm(request.POST, instance=campo))

            elif campo.Tipo == 'C':
                formularios.append(CadenaForm(request.POST, instance=campo))
        print formularios[0]
        if (formularios[0].is_valid()) and (formularios[1].is_valid()):
            a = formularios[0].save()
            b = formularios[1].save(commit=False)
            b.save()

            return HttpResponseRedirect('/desarrollo/proyecto/'+id_proyecto+'/fase/'+id_fase+'/')
    else:
        for campo in atributos:
            if campo.Tipo == 'N':
                formularios.append(NumericoForm(instance=campo))
            elif campo.Tipo == 'C':
                formularios.append(CadenaForm(instance=campo))
    return render_to_response(
        'proyecto/fase/item/com_item.html',
        {'usuario':usuario, 'item':item, 'fase':fase, 'formularios':formularios},
        context_instance=RequestContext(request)
    )

def campos(item):
    for atributo in item.Tipo.Atributos.all():
        if atributo.Tipo=='N':
            object = Numerico(Nombre=atributo.Nombre + "(Numerico)", Dato=0, Tipo='N')
        elif atributo.Tipo=='C':
            object = Cadena(Nombre=atributo.Nombre + "(Cadena)", Dato="", Tipo='C')

        object.save()
        item.Campos.add(object)