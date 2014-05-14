from django.shortcuts import render_to_response, render, HttpResponseRedirect, HttpResponse, RequestContext, get_object_or_404
from administracion.forms import ProyectoForm, UsuarioModForm, UsuarioDelForm, FaseForm, RolForm, AsignarRol
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group, Permission
from administracion.models import Proyecto, Fase, TipoDeItem
from desarrollo.models import *
from desarrollo.forms import *
import reversion
from django.core.exceptions import *

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





@reversion.create_revision()
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
            lista_items = Item.objects.filter(Fase=fase)
            suceso = True
            mensaje = "El item se ha creado exitosamente, no olvides completar los atributos!!"
            return render_to_response(
                'proyecto/fase/des_fase.html',
                {'usuario':usuario, 'fase':fase, 'lista_items':lista_items, 'mensaje':mensaje, 'suceso':suceso},
                context_instance=RequestContext(request)
            )
    else:
        formulario = ItemForm()
    return render_to_response('proyecto/fase/item/crear_item.html',
        {'usuario': usuario, 'formulario': formulario, 'fase': fase, 'lista_tipos':lista_tipos},
        context_instance=RequestContext(request))

@reversion.create_revision()
def mod_item(request, id_proyecto, id_fase, id_item):
    usuario = request.user
    fase = Fase.objects.get(pk=id_fase)
    item = Item.objects.get(pk=id_item)
    formulario = ItemForm(request.POST, instance=item)
    lista_tipos = TipoDeItem.objects.filter(Proyecto=fase.Proyecto)
    if formulario.is_valid():
        formulario.save()
        lista_items = Item.objects.filter(Fase=fase)
        suceso = True
        mensaje = "El item se ha modificado exitosamente"
        return render_to_response(
            'proyecto/fase/des_fase.html',
            {'usuario':usuario, 'fase':fase, 'lista_items':lista_items, 'mensaje':mensaje, 'suceso':suceso},
            context_instance=RequestContext(request)
        )
    else:
        formulario = ItemForm(instance=item)
    return render_to_response(
        'proyecto/fase/item/mod_item.html',
        {'usuario':usuario, 'item':item, 'fase':fase, 'formulario':formulario, 'lista_tipos': lista_tipos},
        context_instance=RequestContext(request)
    )

@reversion.create_revision()
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
        suceso = True
        mensaje = "Atributos modificados exitosamente"
        lista_items = Item.objects.filter(Fase=fase)
        return render_to_response(
            'proyecto/fase/des_fase.html',
            {'usuario':usuario, 'fase':fase, 'lista_items':lista_items, 'mensaje':mensaje, 'suceso':suceso},
            context_instance=RequestContext(request)
        )
    #else:
    return render_to_response(
        'proyecto/fase/item/com_item.html',
        {'usuario':usuario, 'item':item, 'fase':fase, 'campos':campos},
        context_instance=RequestContext(request)
    )

def detalle_item_vista(request, idProyecto, idFase, idItem):
    usuario = request.user
    proyecto = Proyecto.objects.get(pk=idProyecto)
    fase = Fase.objects.get(pk=idFase)
    item = Item.objects.get(pk=idItem)
    campos = Campo.objects.filter(item=item)

    return render_to_response(
        'proyecto/fase/item/detalle.html',
        {'usuario': usuario, 'item': item, 'campos': campos, 'fase':fase},
        context_instance=RequestContext(request)
    )




def historial_item(request, id_proyecto, id_fase, id_item):

    item = Item.objects.get(pk=id_item)
    lista_versiones = reversion.get_unique_for_object(item)
    return render_to_response('proyecto/fase/item/historial_item.html', {'lista_versiones': lista_versiones, 'item':item,
                                                                            'proyecto':Proyecto.objects.get(pk=id_proyecto),
                                                                            'fase': Fase.objects.get(pk=id_fase)},
                              context_instance=RequestContext(request))

def reversion_item(request, id_proyecto,  id_fase, id_item, id_version):
    item = Item.objects.get(pk=id_item)
    lista_version = reversion.get_unique_for_object(item)
    idn_version = int('0'+id_version)
    lista_items = Item.objects.filter(Fase=id_fase)

    for version in lista_version:
        if version.id == idn_version:
            version.revert()
            return render_to_response('proyecto/fase/item/item_exito.html',
                                      {'mensaje': 'Se ha reversionado el atributo a la version '+id_version,
                                       'usuario_actor': request.user, 'proyecto':Proyecto.objects.get(pk=id_proyecto),
                                       'fase': Fase.objects.get(pk=id_fase),
                                       'lista_items': lista_items},
                                      context_instance=RequestContext(request))



    return render_to_response('proyecto/fase/item/item_exito.html',
                                      {'mensaje': 'Se ha',
                                       'usuario_actor': request.user, 'proyecto':Proyecto.objects.get(pk=id_proyecto),
                                       'fase': Fase.objects.get(pk=id_fase),
                                       'lista_items': lista_items},
                                      context_instance=RequestContext(request))


def gestion_relacion_view(request, id_proyecto, id_fase, id_item):
    usuario = request.user
    item = Item.objects.get(pk=id_item)
    fase = Fase.objects.get(pk=id_fase)
    try:
        relacion = Relacion.objects.get(item=item)
    except ObjectDoesNotExist:
        relacion = False
    return render_to_response(
        'proyecto/fase/relacion/gestion_relaciones.html',
        {'usuario': usuario, 'relacion': relacion, 'item': item, 'fase': fase},
        context_instance=RequestContext(request)
    )


def asignar_padre_view(request, id_proyecto, id_fase, id_item):
    usuario = request.user
    item = Item.objects.get(pk=id_item)
    fase = Fase.objects.get(pk=id_fase)
    try:
        relacion = Relacion.objects.get(item=item)
    except ObjectDoesNotExist:
        relacion = None
    lista_items = Item.objects.filter(Fase=fase).exclude(pk=id_item)
    nueva_relacion = Relacion()
    nueva_relacion.item = item
    if request.method=='POST':
        formulario = PadreForm(request.POST, instance=nueva_relacion)
        if formulario.is_valid():
            if(relacion != None):
                relacion.delete()
            formulario.save()
            relacion = Relacion.objects.get(item=item)
            mensaje = 'Padre asignado exitosamente'
            suceso = True
            return render_to_response(
                'proyecto/fase/relacion/gestion_relaciones.html',
                {'usuario': usuario, 'fase': fase, 'mensaje': mensaje, 'suceso': suceso, 'item': item, 'relacion':relacion},
                context_instance=RequestContext(request)
            )
    else:
        formulario = PadreForm()
    return render_to_response(
        'proyecto/fase/relacion/asignar_padre.html',
        {'formulario': formulario, 'fase': fase, 'usuario': usuario, 'relacion': relacion, 'lista_items':lista_items, 'item': item},
        context_instance=RequestContext(request)
    )


def asignar_antecesor_view(request, id_proyecto, id_fase, id_item):
    usuario = request.user
    item = Item.objects.get(pk=id_item)
    fase = Fase.objects.get(pk=id_fase)
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    try:
        relacion = Relacion.objects.get(item=item)
    except ObjectDoesNotExist:
        relacion = None
    if fase.Numero != 1:
        faseAnterior = Fase.objects.get(Proyecto=proyecto, Numero=fase.Numero-1)
        lista_items = Item.objects.filter(Fase=faseAnterior)
    nueva_relacion = Relacion()
    nueva_relacion.item = item
    if request.method=='POST':
        formulario = AntecesorForm(request.POST, instance=nueva_relacion)
        if formulario.is_valid():
            if(relacion != None):
                relacion.delete()
            formulario.save()
            mensaje = 'Antecesor asignado exitosamente'
            suceso = True
            relacion = Relacion.objects.get(item=item)
            return render_to_response(
                'proyecto/fase/relacion/gestion_relaciones.html',
                {'usuario':usuario, 'fase':fase, 'mensaje':mensaje, 'suceso':suceso, 'item': item, 'relacion': relacion},
                context_instance=RequestContext(request)
            )
    else:
        formulario = AntecesorForm()

    return render_to_response(
        'proyecto/fase/relacion/asignar_antecesor.html',
        {'formulario': formulario, 'fase': fase, 'usuario': usuario, 'relacion': relacion, 'lista_items':lista_items, 'item': item},
        context_instance=RequestContext(request)
    )

def gestion_archivos_view(request, id_proyecto, id_fase, id_item):
    usuario = request.user
    fase = Fase.objects.get(pk=id_fase)
    item = Item.objects.get(pk=id_item)
    lista_archivos = Archivo.objects.filter(item=item)
    return render_to_response(
        'proyecto/fase/archivo/gestion_archivos.html',
        {'fase': fase, 'usuario': usuario, 'item': item, 'lista_archivos': lista_archivos},
        context_instance=RequestContext(request)
    )


def agregar_archivo_view(request, id_proyecto, id_fase, id_item):
    usuario = request.user
    fase = Fase.objects.get(pk=id_fase)
    item = Item.objects.get(pk=id_item)
    archivo = Archivo()
    archivo.item = item
    if request.method == 'POST':
        formulario = ArchivoForm(request.POST, request.FILES or None, instance=archivo)

        print formulario.is_valid()
        if formulario.is_valid():
            formulario.save()
            mensaje = 'Archivo asignado exitosamente'
            suceso = True
            lista_archivos = Archivo.objects.filter(item=item)
            return  render_to_response(
                'proyecto/fase/archivo/gestion_archivos.html',
                {'usuario':usuario, 'fase':fase, 'mensaje':mensaje, 'suceso':suceso,
                 'item': item, 'lista_archivos': lista_archivos},
                context_instance=RequestContext(request)
            )
    else:
        formulario = ArchivoForm()
    return  render_to_response(
        'proyecto/fase/archivo/agregar_archivo.html',
        {'formulario': formulario, 'fase': fase, 'usuario': usuario, 'item': item},
        context_instance=RequestContext(request)
    )

def detalle_fase(request, id_proyecto, id_fase):
    """

    :param request:
    :param id_fase:
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
    fase = Fase.objects.get(pk=id_fase)
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    return render_to_response('proyecto/fase/detalle.html',
                              {'usuario_actor': usuario_actor, 'fase': fase, 'proyecto':proyecto},
                              context_instance=RequestContext(request))

def sucesores(item):
    sucesores = Relacion.objects.filter(antecesor=item)
    return sucesores

def hijos(item):
    hijos = Relacion.objects.filter(padre=item)
    return hijos