from django.shortcuts import render_to_response, render, HttpResponseRedirect, HttpResponse, RequestContext, get_object_or_404
from django.contrib.auth.decorators import login_required
from desarrollo.forms import *
import reversion
from django.core.exceptions import *
import pydot

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
    return render_to_response('desarrollo.html', {'lista_proyectos': lista_proyectos, 'usuario_actor': usuario},
                              context_instance=RequestContext(request))


def des_proyecto(request, id_proyecto):
    generar_grafo_proyecto(id_proyecto)
    usuario = request.user
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    lista_fases = Fase.objects.filter(Proyecto=id_proyecto)
    lista_items = []
    for fase in lista_fases:
        lista_items = Item.objects.filter(Fase=fase)
        if lista_items:
            break
    return render_to_response('proyecto/des_proyecto.html',
        {'usuario_actor': usuario, 'proyecto': proyecto, 'lista_fases': lista_fases, 'lista_items':lista_items},
        context_instance=RequestContext(request))

def des_fase(request, id_proyecto, id_fase):
    generar_grafo_fase(id_fase)
    usuario = request.user
    fase = Fase.objects.get(pk=id_fase)
    lista_items = Item.objects.filter(Fase=fase)
    return render_to_response('proyecto/fase/des_fase.html',
        {'usuario_actor': usuario, 'fase': fase, 'lista_items': lista_items},
        context_instance=RequestContext(request))





@reversion.create_revision()
def crear_item(request, id_proyecto, id_fase):
    usuario = request.user
    fase = Fase.objects.get(pk=id_fase)
    item = Item(Usuario=usuario, Fase=fase, Version=1)
    lista_tipos = TipoDeItem.objects.filter(Fase=fase)

    if fase.Proyecto.Estado == 'P':
        mensaje = 'No puedes crear items en el proyecto '+fase.Proyecto.Nombre+' porque no ha iniciado'
        suceso = False
        return render_to_response(
                'proyecto/fase/des_fase.html',
                {'usuario_actor':usuario, 'fase':fase, 'mensaje':mensaje, 'suceso':suceso},
                context_instance=RequestContext(request)
            )
    elif fase.Proyecto.Estado == 'F':
        mensaje = 'No puedes crear items en el proyecto '+fase.Proyecto.Nombre+' porque ha finalizado'
        suceso = False
        return render_to_response(
                'proyecto/fase/des_fase.html',
                {'usuario_actor':usuario, 'fase':fase, 'mensaje':mensaje, 'suceso':suceso},
                context_instance=RequestContext(request)
            )
    elif fase.Proyecto.Estado == 'C':
        mensaje = 'No puedes crear items en el proyecto '+fase.Proyecto.Nombre+' porque ha sido cancelado'
        suceso = False
        return render_to_response(
                'proyecto/fase/des_fase.html',
                {'usuario_actor':usuario, 'fase':fase, 'mensaje':mensaje, 'suceso':suceso},
                context_instance=RequestContext(request)
            )
    elif request.method == 'POST':
        formulario = ItemForm(request.POST, instance=item)
        if formulario.is_valid():
            formulario.save()
            item = Item.objects.last()
            for atributo in item.Tipo.Atributos.all():
                campo = Campo.objects.create(item=item, tipoItem=item.Tipo, atributo=atributo)
                campo.save()
            lista_items = Item.objects.filter(Fase=fase)
            suceso = True
            mensaje = "El item se ha creado exitosamente, no olvides completar los atributos!!"
            generar_grafo_fase(id_fase)
            return render_to_response(
                'proyecto/fase/des_fase.html',
                {'usuario_actor':usuario, 'fase':fase, 'lista_items':lista_items, 'mensaje':mensaje, 'suceso':suceso},
                context_instance=RequestContext(request)
            )
    else:
        formulario = ItemForm(instance=item)
    return render_to_response('proyecto/fase/item/crear_item.html',
        {'usuario_actor': usuario, 'formulario': formulario, 'fase': fase, 'lista_tipos':lista_tipos},
        context_instance=RequestContext(request))

@reversion.create_revision()
def mod_item(request, id_proyecto, id_fase, id_item):
    usuario = request.user
    fase = Fase.objects.get(pk=id_fase)
    item = Item.objects.get(pk=id_item)
    formulario = ItemForm(request.POST, instance=item)
    lista_tipos = TipoDeItem.objects.filter(Fase=fase)
    if formulario.is_valid():
        formulario.save()
        lista_items = Item.objects.filter(Fase=fase)
        suceso = True
        mensaje = "El item se ha modificado exitosamente"
        generar_grafo_fase(id_fase)
        return render_to_response(
            'proyecto/fase/des_fase.html',
            {'usuario_actor':usuario, 'fase':fase, 'lista_items':lista_items, 'mensaje':mensaje, 'suceso':suceso},
            context_instance=RequestContext(request)
        )
    else:
        formulario = ItemForm(instance=item)
    return render_to_response(
        'proyecto/fase/item/mod_item.html',
        {'usuario_actor':usuario, 'item':item, 'fase':fase, 'formulario':formulario, 'lista_tipos': lista_tipos},
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
        item.save()
        lista_items = Item.objects.filter(Fase=fase)
        return render_to_response(
            'proyecto/fase/des_fase.html',
            {'usuario_actor':usuario, 'fase':fase, 'lista_items':lista_items, 'mensaje':mensaje, 'suceso':suceso},
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
        {'usuario_actor': usuario, 'item': item, 'campos': campos, 'fase':fase},
        context_instance=RequestContext(request)
    )

def conf_eliminar_item(request, idProyecto, idFase, idItem):
    usuario = request.user
    proyecto = Proyecto.objects.get(pk=idProyecto)
    fase = Fase.objects.get(pk=idFase)
    item = Item.objects.get(pk=idItem)
    return render_to_response(
        'proyecto/fase/item/conf_eliminar_item.html',
        {'usuario_actor': usuario, 'item': item, 'fase': fase},
        context_instance=RequestContext(request)
    )


def eliminar_item(request, idProyecto, idFase, idItem):
    usuario = request.user
    proyecto = Proyecto.objects.get(pk=idProyecto)
    fase = Fase.objects.get(pk=idFase)
    item = Item.objects.get(pk=idItem)
    campos = Campo.objects.filter(item=item)
    relacion = Relacion.objects.filter(item=item)
    item_nombre = item.Nombre
    item.delete()
    campos.delete()
    relacion.delete()
    lista_items = Item.objects.filter(Fase=idFase)
    generar_grafo_fase(idFase)
    return render_to_response(
        'proyecto/fase/item/item_exito.html',
        {'usuario_actor': usuario, 'fase': fase,'lista_items':lista_items,
         'mensaje': 'El item '+item_nombre+' se ha eliminado exitosamente'},
        context_instance=RequestContext(request)
    )

def generar_grafo_proyecto(id_proyecto):
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    fases_proyecto = Fase.objects.filter(Proyecto=proyecto)
    relaciones_proyecto = []
    grafo = pydot.Dot(graph_type='digraph', rankdir="LR",labelloc='b', labeljust='r', ranksep=1)
    grafo.set_node_defaults(shape="record")
    grafo.set_edge_defaults(color="blue", arrowhead="vee", weight="1")
    for fase in fases_proyecto:
        cluster = pydot.Cluster(graph_name=fase.Nombre,label=fase.Nombre, style='filled',color='lightgrey')
        items_fase = Item.objects.filter(Fase=fase)
        for item in items_fase:
            cluster.add_node(pydot.Node(name=item.Nombre, label = "<f0>%s|<f1>Costo $: %d"%(item.Nombre,item.CostoUnitario)
                                        , style="filled", fillcolor="white"))
            if Relacion.objects.filter(item=item):
                relaciones_proyecto.append(Relacion.objects.get(item=item))
        grafo.add_subgraph(cluster)
    for relacion in relaciones_proyecto:
        if relacion.padre:
            grafo.add_edge(pydot.Edge(src=relacion.padre.Nombre,dst=relacion.item.Nombre,label="%d"%relacion.padre.CostoUnitario,color="blue"))
        if relacion.antecesor:
            grafo.add_edge(pydot.Edge(src=relacion.antecesor.Nombre,dst=relacion.item.Nombre,label="%d"%relacion.antecesor.CostoUnitario,color="green"))
    grafo.write_png('static/media/grafoProyectoActual.png')

def generar_grafo_fase(id_fase):
    fase = Fase.objects.get(pk=id_fase)
    relaciones_fase = []
    grafo = pydot.Dot(graph_type='digraph', rankdir="LR",labelloc='b', labeljust='r', ranksep=1)
    grafo.set_node_defaults(shape="component")
    grafo.set_edge_defaults(arrowhead="vee", weight="0")
    cluster = pydot.Cluster(graph_name=fase.Nombre,label=fase.Nombre, style='filled',color='lightgrey')
    items_fase = Item.objects.filter(Fase=fase)
    for item in items_fase:
        cluster.add_node(pydot.Node(name=item.Nombre, style="filled", fillcolor="white"))
        if Relacion.objects.filter(item=item):
            relaciones_fase.append(Relacion.objects.get(item=item))
    grafo.add_subgraph(cluster)
    for relacion in relaciones_fase:
        if relacion.padre:
            grafo.add_edge(pydot.Edge(src=relacion.padre.Nombre,dst=relacion.item.Nombre,color="blue"))
    grafo.write_png('static/media/grafoFaseActual.png')


def historial_item(request, id_proyecto, id_fase, id_item):
    item = Item.objects.get(pk=id_item)
    lista_versiones = reversion.get_for_object(item)
    lista_atributos = Campo.objects.filter(item=item)
    return render_to_response('proyecto/fase/item/historial_item.html', {'lista_versiones': lista_versiones, 'item':item,
                                                                            'proyecto':Proyecto.objects.get(pk=id_proyecto),
                                                                            'fase': Fase.objects.get(pk=id_fase)},
                              context_instance=RequestContext(request))

def reversion_item(request, id_proyecto,  id_fase, id_item, id_version):
    item = Item.objects.get(pk=id_item)
    lista_version = reversion.get_unique_for_object(item)
    lista_atributos = Campo.objects.filter(item=item)
    idn_version = int('0'+id_version)
    lista_items = Item.objects.filter(Fase=id_fase)
    version_item = 0

    for version in lista_version:
        if version.id == idn_version:
            version.revert()
            version_item = version.revision_id

    for atributo in lista_atributos:
        lista_version = reversion.get_unique_for_object(atributo)
        for version in lista_version:
            if version.revision_id == version_item:
                version.revert()

    return render_to_response('proyecto/fase/item/item_exito.html',
                                      {'mensaje': 'Se ha reversionado el atributo a la version '+id_version,
                                       'usuario_actor': request.user, 'proyecto':Proyecto.objects.get(pk=id_proyecto),
                                       'fase': Fase.objects.get(pk=id_fase),
                                       'lista_items': lista_items},
                                      context_instance=RequestContext(request))

def detalle_item_version(request, idProyecto, idFase, idItem, idVersion):
    usuario = request.user
    fase = Fase.objects.get(pk=idFase)
    item = Item.objects.get(pk=idItem)
    lista_version = reversion.get_unique_for_object(item)
    lista_atributos = Campo.objects.filter(item=item)
    idn_version = int('0'+idVersion)
    id = 0
    campos = []

    for version in lista_version:
        if version.id == idn_version:
            item = version
            id = version.revision_id

    for atributo in lista_atributos:
        lista_version = reversion.get_unique_for_object(atributo)
        for version in lista_version:
            if version.revision_id == id:
                campos.append(version)

    for x in campos:
        print(x.item)

    return render_to_response(
        'proyecto/fase/item/detalle_version.html',
        {'usuario_actor': usuario, 'item': item, 'campos': campos, 'fase':fase},
        context_instance=RequestContext(request)
    )


@reversion.create_revision()
def gestion_relacion_view(request, id_proyecto, id_fase, id_item):
    usuario = request.user
    item = Item.objects.get(pk=id_item)
    fase = Fase.objects.get(pk=id_fase)
    try:
        relacion = Relacion.objects.get(item=item)
    except ObjectDoesNotExist:
        relacion = False
    lista_hijos = hijos(item)
    lista_sucesores = sucesores(item)
    return render_to_response(
        'proyecto/fase/relacion/gestion_relaciones.html',
        {'usuario_actor': usuario, 'relacion': relacion, 'item': item, 'fase': fase,
         'hijos': lista_hijos, 'sucesores': lista_sucesores},
        context_instance=RequestContext(request)
    )

@reversion.create_revision()
def asignar_padre_view(request, id_proyecto, id_fase, id_item):
    usuario = request.user
    item = Item.objects.get(pk=id_item)
    fase = Fase.objects.get(pk=id_fase)
    try:
        relacion = Relacion.objects.get(item=item)
    except ObjectDoesNotExist:
        relacion = False

    lista_items = Item.objects.filter(Fase=fase).exclude(pk=id_item)
    nueva_relacion = Relacion()
    nueva_relacion.item = item
    if request.method=='POST':
        formulario = PadreForm(request.POST, instance=nueva_relacion)
        if formulario.is_valid():
            if generaCiclo(id_item, request.POST['padre']):
                suceso = False
                mensaje = 'Error: Esta relacion genera un ciclo'
            else:
                if(relacion != False):
                    relacion.delete()
                formulario.save()
                item.save()
                relacion = Relacion.objects.get(item=item)

                mensaje = 'Padre asignado exitosamente'
                suceso = True
            return render_to_response(
                'proyecto/fase/relacion/gestion_relaciones.html',
                {'usuario': usuario, 'fase': fase, 'mensaje': mensaje, 'suceso': suceso, 'item': item,
                 'relacion': relacion},
                context_instance=RequestContext(request)
            )
    else:
        formulario = PadreForm()
    return render_to_response(
        'proyecto/fase/relacion/asignar_padre.html',
        {'formulario': formulario, 'fase': fase, 'usuario_actor': usuario, 'relacion': relacion, 'lista_items':lista_items, 'item': item},
        context_instance=RequestContext(request)
    )

def generaCiclo(id_item,id_padre):
    itemPadre = Item.objects.get(pk=id_padre)
    id_item = int(id_item)
    while(itemPadre):
        if itemPadre.pk == id_item:
            return True
        try:
            relacion = Relacion.objects.get(item=itemPadre)
            itemPadre = relacion.padre
        except:
            return False
    return False


@reversion.create_revision()
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
            item.save()
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
        {'formulario': formulario, 'fase': fase, 'usuario_actor': usuario, 'relacion': relacion, 'lista_items':lista_items, 'item': item},
        context_instance=RequestContext(request)
    )

@reversion.create_revision()
def gestion_archivos_view(request, id_proyecto, id_fase, id_item):
    usuario = request.user
    fase = Fase.objects.get(pk=id_fase)
    item = Item.objects.get(pk=id_item)
    lista_archivos = Archivo.objects.filter(item=item)
    return render_to_response(
        'proyecto/fase/archivo/gestion_archivos.html',
        {'fase': fase, 'usuario_actor': usuario, 'item': item, 'lista_archivos': lista_archivos},
        context_instance=RequestContext(request)
    )

@reversion.create_revision()
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
                {'usuario_actor':usuario, 'fase':fase, 'mensaje':mensaje, 'suceso':suceso,
                 'item': item, 'lista_archivos': lista_archivos},
                context_instance=RequestContext(request)
            )
    else:
        formulario = ArchivoForm()
    return render_to_response(
        'proyecto/fase/archivo/agregar_archivo.html',
        {'formulario': formulario, 'fase': fase, 'usuario_actor': usuario, 'item': item},
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

def impacto_view(request, id_proyecto, id_fase, id_item):
    usuario = request.user
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    fase = Fase.objects.get(pk=id_fase)
    item = Item.objects.get(pk=id_item)
    costo_m_atras = costo_monetario_atras(item)
    costo_m_adelante = costo_monetario_adelante(item)
    costo_t_atras = costo_temporal_atras(item)
    costo_t_adelante = costo_temporal_adelante(item)
    return render_to_response(
        'proyecto/fase/item/impacto.html',
        {'fase': fase, 'usuario': usuario, 'item': item, 'costo_monetario_atras': costo_m_atras,
         'costo_monetario_adelante': costo_m_adelante, 'costo_temporal_atras': costo_t_atras,
         'costo_temporal_adelante': costo_t_adelante},
        context_instance=RequestContext(request)
    )



def costo_monetario_atras(item):
    cont = 0
    try:
        relacion = Relacion.objects.get(item=item)
        if relacion.padre != None:
            cont += relacion.padre.CostoUnitario
            cont += costo_monetario_atras(relacion.padre)
        elif relacion.antecesor != None:
            cont += relacion.antecesor.CostoUnitario
            cont += costo_monetario_atras(relacion.antecesor)
    except ObjectDoesNotExist:
        return 0
    return cont

def costo_monetario_adelante(item):
    cont = 0
    lista_hijos = hijos(item)
    lista_sucesores = sucesores(item)
    for a in lista_hijos:
        cont += a.item.CostoUnitario
        cont += costo_monetario_adelante(a.item)
    for b in lista_sucesores:
        cont += b.item.CostoUnitario
        cont += costo_monetario_adelante(b.item)
    return cont

def costo_temporal_atras(item):
    cont = 0
    try:
        relacion = Relacion.objects.get(item=item)
        if relacion.padre != None:
            cont += relacion.padre.CostoTemporal
            cont += costo_temporal_atras(relacion.padre)
        elif relacion.antecesor != None:
            cont += relacion.antecesor.CostoTemporal
            cont += costo_temporal_atras(relacion.antecesor)
    except ObjectDoesNotExist:
        return 0
    return cont

def costo_temporal_adelante(item):
    cont = 0
    lista_hijos = hijos(item)
    lista_sucesores = sucesores(item)
    for a in lista_hijos:
        cont += a.item.CostoTemporal
        cont += costo_temporal_adelante(a.item)
    for b in lista_sucesores:
        cont += b.item.CostoTemporal
        cont += costo_temporal_adelante(b.item)
    return cont

def eliminar_relacion_view(request, id_proyecto, id_fase, id_item):
    usuario = request.user
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    fase = Fase.objects.get(pk=id_fase)
    item = Item.objects.get(pk=id_item)
    return render_to_response(
        'proyecto/fase/relacion/eliminar.html',
        {'usuario': usuario, 'fase': fase, 'item': item},
        context_instance=RequestContext(request)
    )

def relacion_eliminada_view(request, id_proyecto, id_fase, id_item):
    usuario = request.user
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    fase = Fase.objects.get(pk=id_fase)
    item = Item.objects.get(pk=id_item)
    relacion = Relacion.objects.get(item=item)
    relacion.delete()
    relacion = False
    suceso = True
    mensaje = 'Relacion eliminada con exito'
    return render_to_response(
        'proyecto/fase/relacion/gestion_relaciones.html',
        {'usuario': usuario, 'fase': fase, 'item': item, 'suceso': suceso, 'mensaje': mensaje, 'relacion': relacion},
        context_instance=RequestContext(request)
    )

def finalizar_item_view(request, id_proyecto, id_fase, id_item):
    usuario = request.user
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    fase = Fase.objects.get(pk=id_fase)
    item = Item.objects.get(pk=id_item)
    return render_to_response(
        'proyecto/fase/item/finalizar.html',
        {'usuario': usuario, 'fase': fase, 'item': item},
        context_instance=RequestContext(request)
    )

def item_finalizado_view(request, id_proyecto, id_fase, id_item):
    usuario = request.user
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    fase = Fase.objects.get(pk=id_fase)
    item = Item.objects.get(pk=id_item)
    item.Estado = item.FINALIZADO
    item.save()
    suceso = True
    mensaje = 'Item finalizado exitosamente'
    lista_items = Item.objects.filter(Fase=fase)
    return render_to_response(
        'proyecto/fase/des_fase.html',
        {'usuario': usuario, 'fase': fase, 'item': item, 'suceso': suceso, 'mensaje': mensaje, 'lista_items': lista_items},
        context_instance=RequestContext(request)
    )
