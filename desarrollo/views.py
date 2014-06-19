from django.shortcuts import render_to_response, render, HttpResponseRedirect, HttpResponse, RequestContext, get_object_or_404
from django.contrib.auth.decorators import login_required
from desarrollo.forms import *
import reversion
from django.core.exceptions import *
from django.db import IntegrityError
import pydot
from gestion.forms import *
from gestion.models import *
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

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
    return render_to_response('des_proyecto.html',
        {'usuario_actor': usuario, 'proyecto': proyecto, 'lista_fases': lista_fases, 'lista_items':lista_items},
        context_instance=RequestContext(request))

def des_fase(request, id_proyecto, id_fase):
    generar_grafo_fase(id_fase)
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    usuario = request.user
    fase = Fase.objects.get(pk=id_fase)
    lista_items = Item.objects.filter(Fase=fase).exclude(condicion=Item.ELIMINADO)
    try:
        comite = ComiteDeCambio.objects.get(Proyecto=proyecto)
    except ObjectDoesNotExist:
        comite = False
    items_validados = Item.objects.filter(Fase=fase).filter(Estado=Item.VALIDADO)
    if items_validados == None:
        items_validados = True

    p_consultar = usuario.tienePermisoProyecto("consulta_item",id_proyecto)
    p_revivir = usuario.tienePermisoProyecto("revive_item",id_proyecto)
    p_aprobar = usuario.tienePermisoProyecto("aprueba_item",id_proyecto)
    p_desaprobar = usuario.tienePermisoProyecto("desaprueba_item",id_proyecto)
    p_eliminar_item = usuario.tienePermisoProyecto("delete_item",id_proyecto)
    p_gestionar_item = usuario.tienePermisoProyecto("change_item",id_proyecto)
    p_crear_item = usuario.tienePermisoProyecto("add_item",id_proyecto)
    p_solicitar_cambio = usuario.tienePermisoProyecto("solicita_item",id_proyecto)

    return render_to_response('des_fase.html',
        {'usuario_actor': usuario, 'fase': fase, 'lista_items': lista_items,
         'comite': comite, 'validados': items_validados, 'p_consultar':p_consultar, 'p_revivir':p_revivir, 'p_aprobar':p_aprobar,
         'p_desaprobar': p_desaprobar, 'p_eliminar_item':p_eliminar_item, 'p_gestionar_item':p_gestionar_item,'p_crear_item':p_crear_item,
         'p_solicitar_cambio':p_solicitar_cambio},
        context_instance=RequestContext(request))


@reversion.create_revision()
def crear_item(request, id_proyecto, id_fase):
    usuario = request.user
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    fase = Fase.objects.get(pk=id_fase)
    item = Item(Usuario=usuario, Fase=fase, Version=1)
    lista_tipos = TipoDeItem.objects.filter(Fase=fase)

    if fase.Proyecto.Estado == 'P':
        mensaje = 'No puedes crear items en el proyecto '+fase.Proyecto.Nombre+' porque no ha iniciado'
        suceso = False
        return render_to_response(
            'des_fase.html',
                {'usuario_actor':usuario, 'fase':fase, 'mensaje':mensaje, 'suceso':suceso},
                context_instance=RequestContext(request)
            )
    elif fase.Proyecto.Estado == 'F':
        mensaje = 'No puedes crear items en el proyecto '+fase.Proyecto.Nombre+' porque ha finalizado'
        suceso = False
        return render_to_response(
            'des_fase.html',
                {'usuario_actor':usuario, 'fase':fase, 'mensaje':mensaje, 'suceso':suceso},
                context_instance=RequestContext(request)
            )
    elif fase.Proyecto.Estado == 'C':
        mensaje = 'No puedes crear items en el proyecto '+fase.Proyecto.Nombre+' porque ha sido cancelado'
        suceso = False
        return render_to_response(
            'des_fase.html',
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
            lista_items = Item.objects.filter(Fase=fase).exclude(condicion=Item.ELIMINADO)
            relacion = Relacion.objects.create(item=item)
            relacion.save()
            suceso = True
            mensaje = "El item se ha creado exitosamente, no olvides completar los atributos"
            generar_grafo_fase(id_fase)
            p_consultar = usuario.tienePermisoProyecto("consulta_item",id_proyecto)
            p_revivir = usuario.tienePermisoProyecto("revive_item",id_proyecto)
            p_aprobar = usuario.tienePermisoProyecto("aprueba_item",id_proyecto)
            p_desaprobar = usuario.tienePermisoProyecto("desaprueba_item",id_proyecto)
            p_eliminar_item = usuario.tienePermisoProyecto("delete_item",id_proyecto)
            p_gestionar_item = usuario.tienePermisoProyecto("change_item",id_proyecto)
            p_crear_item = usuario.tienePermisoProyecto("add_item",id_proyecto)
            p_solicitar_cambio = usuario.tienePermisoProyecto("solicita_item",id_proyecto)
            try:
                comite = ComiteDeCambio.objects.get(Proyecto=fase.Proyecto.id)
            except ObjectDoesNotExist:
                comite = False
            items_validados = Item.objects.filter(Fase=fase).filter(Estado=Item.VALIDADO)
            if items_validados == None:
                items_validados = True

            return render_to_response('des_fase.html',
                {'usuario_actor': usuario, 'fase': fase, 'lista_items': lista_items,
                 'comite': comite, 'validados': items_validados, 'p_consultar':p_consultar, 'p_revivir':p_revivir, 'p_aprobar':p_aprobar,
                 'p_desaprobar': p_desaprobar, 'p_eliminar_item':p_eliminar_item, 'p_gestionar_item':p_gestionar_item,'p_crear_item':p_crear_item,
                 'p_solicitar_cambio':p_solicitar_cambio, 'suceso': suceso, 'mensaje': mensaje},
                context_instance=RequestContext(request))
    else:
        formulario = ItemForm(instance=item)
    return render_to_response('item/crear_item.html',
        {'usuario_actor': usuario, 'formulario': formulario, 'fase': fase, 'lista_tipos':lista_tipos},
        context_instance=RequestContext(request))

@reversion.create_revision()
def mod_item(request, id_proyecto, id_fase, id_item):
    usuario = request.user
    fase = Fase.objects.get(pk=id_fase)
    item = Item.objects.get(pk=id_item)
    item.Version += 1

    lista_tipos = TipoDeItem.objects.filter(Fase=fase)
    relacion = Relacion.objects.get(item=item)
    campos = Campo.objects.filter(item=item)
    if item.Estado == Item.CREDENCIAL:
        solicitudes = SolicitudCambio.objects.filter(usuario=usuario, estado=SolicitudCambio.ACEPTADA, fase=fase)
        boolean = False
        for solicitud in solicitudes:
            if solicitud.items.all().filter(pk=id_item):
                boolean = True

        if boolean == False:
            suceso = False
            mensaje = 'Usted no posee permiso para modificar este item'
            lista_items = Item.objects.filter(Fase=fase).exclude(condicion=Item.ELIMINADO)
            return render_to_response(
                'des_fase.html',
                {'usuario_actor': usuario, 'fase': fase, 'lista_items': lista_items,
                 'mensaje': mensaje, 'suceso': suceso},
                context_instance=RequestContext(request)
            )

    if item.Estado == Item.CREDENCIAL:
        item.Estado = Item.VALIDADO
    formulario1 = ModItemForm(request.POST, instance=item)
    if formulario1.is_valid():
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

        formulario1.save()
        lista_items = Item.objects.filter(Fase=fase).exclude(condicion=Item.ELIMINADO)
        suceso = True
        relacion.save()
        mensaje = "El item se ha modificado exitosamente"
        generar_grafo_fase(id_fase)
        p_consultar = usuario.tienePermisoProyecto("consulta_item", id_proyecto)
        p_revivir = usuario.tienePermisoProyecto("revive_item", id_proyecto)
        p_aprobar = usuario.tienePermisoProyecto("aprueba_item", id_proyecto)
        p_desaprobar = usuario.tienePermisoProyecto("desaprueba_item", id_proyecto)
        p_eliminar_item = usuario.tienePermisoProyecto("delete_item", id_proyecto)
        p_gestionar_item = usuario.tienePermisoProyecto("change_item", id_proyecto)
        p_crear_item = usuario.tienePermisoProyecto("add_item", id_proyecto)
        p_solicitar_cambio = usuario.tienePermisoProyecto("solicita_item", id_proyecto)
        try:
            comite = ComiteDeCambio.objects.get(Proyecto=fase.Proyecto.id)
        except ObjectDoesNotExist:
            comite = False
        items_validados = Item.objects.filter(Fase=fase).filter(Estado=Item.VALIDADO)
        if items_validados == None:
            items_validados = True
        return render_to_response('des_fase.html',
            {'usuario_actor': usuario, 'fase': fase, 'lista_items': lista_items,
             'comite': comite, 'validados': items_validados, 'p_consultar':p_consultar, 'p_revivir':p_revivir, 'p_aprobar':p_aprobar,
             'p_desaprobar': p_desaprobar, 'p_eliminar_item':p_eliminar_item, 'p_gestionar_item':p_gestionar_item,'p_crear_item':p_crear_item,
             'p_solicitar_cambio':p_solicitar_cambio, 'mensaje': mensaje, 'suceso': suceso},
            context_instance=RequestContext(request))
    else:
        formulario1 = ModItemForm(instance=item)
    return render_to_response(
        'item/mod_item.html',
        {'usuario_actor': usuario, 'item': item, 'fase': fase, 'formulario': formulario1,
         'lista_tipos': lista_tipos, 'campos': campos},
        context_instance=RequestContext(request)
    )

@reversion.create_revision()
def completar_item(request, id_proyecto, id_fase, id_item):
    usuario = request.user
    fase = Fase.objects.get(pk=id_fase)
    item = Item.objects.get(pk=id_item)
    relacion = Relacion.objects.get(item=item)
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
        item.Version += 1
        item.save()
        relacion.save()
        generar_grafo_fase(id_fase)
        lista_items = Item.objects.filter(Fase=fase).exclude(condicion=Item.ELIMINADO)
        return render_to_response(
            'des_fase.html',
            {'usuario_actor':usuario, 'fase':fase, 'lista_items':lista_items, 'mensaje':mensaje, 'suceso':suceso},
            context_instance=RequestContext(request)
        )
    #else:
    return render_to_response(
        'item/com_item.html',
        {'usuario':usuario, 'item':item, 'fase':fase, 'campos':campos},
        context_instance=RequestContext(request)
    )

def detalle_item_vista(request, idProyecto, idFase, idItem):
    usuario = request.user
    proyecto = Proyecto.objects.get(pk=idProyecto)
    fase = Fase.objects.get(pk=idFase)
    item = Item.objects.get(pk=idItem)
    campos = Campo.objects.filter(item=item)
    relacion = Relacion.objects.get(item=item)
    lista_hijos = hijos(item)
    lista_sucesores =sucesores(item)
    return render_to_response(
        'item/detalle.html',
        {'usuario_actor': usuario, 'item': item, 'campos': campos, 'fase':fase, 'relacion': relacion,
         'hijs': lista_hijos, 'sucesores': lista_sucesores},
        context_instance=RequestContext(request)
    )



def conf_eliminar_item(request, idProyecto, idFase, idItem):
    usuario = request.user
    fase = Fase.objects.get(pk=idFase)
    item = Item.objects.get(pk=idItem)
    lista_items = Item.objects.filter(Fase=fase).exclude(condicion=Item.ELIMINADO)
    """
    if hijos(item) or sucesores(item):
        mensaje = 'El item '+item.Nombre+' no se puede eliminar porque posee hijos o sucesores'
        suceso = False
        generar_grafo_fase(idFase)
        p_consultar = usuario.tienePermisoProyecto("consulta_item", idProyecto)
        p_revivir = usuario.tienePermisoProyecto("revive_item", idProyecto)
        p_aprobar = usuario.tienePermisoProyecto("aprueba_item",idProyecto)
        p_desaprobar = usuario.tienePermisoProyecto("desaprueba_item",idProyecto)
        p_eliminar_item = usuario.tienePermisoProyecto("delete_item",idProyecto)
        p_gestionar_item = usuario.tienePermisoProyecto("change_item",idProyecto)
        p_crear_item = usuario.tienePermisoProyecto("add_item",idProyecto)
        p_solicitar_cambio = usuario.tienePermisoProyecto("solicita_item",idProyecto)
        try:
            comite = ComiteDeCambio.objects.get(Proyecto=fase.Proyecto.id)
        except ObjectDoesNotExist:
            comite = False
        items_validados = Item.objects.filter(Fase=fase).filter(Estado=Item.VALIDADO)
        if items_validados == None:
            items_validados = True

        return render_to_response(
        'des_fase.html',
        {'usuario_actor': usuario, 'fase': fase,'lista_items':lista_items,'p_consultar':p_consultar, 'p_revivir':p_revivir, 'p_aprobar':p_aprobar,
         'p_desaprobar': p_desaprobar, 'p_eliminar_item':p_eliminar_item, 'p_gestionar_item':p_gestionar_item,'p_crear_item':p_crear_item,'comite': comite, 'validados': items_validados,
         'p_solicitar_cambio':p_solicitar_cambio,'mensaje': mensaje, 'suceso':suceso}, context_instance=RequestContext(request)
        )
    else:
    """
    return render_to_response(
        'item/conf_eliminar_item.html',
        {'usuario_actor': usuario, 'item': item, 'fase': fase},
        context_instance=RequestContext(request)
    )

def eliminar_item(request, idProyecto, idFase, idItem):
    usuario = request.user
    fase = Fase.objects.get(pk=idFase)
    item = Item.objects.get(pk=idItem)

    relacion = Relacion.objects.get(item=item)
    relacion.estado = Relacion.ELIMINADO
    relacion.save()

    item.condicion = Item.ELIMINADO
    item.save()

    #Seteamos las relaciones de los hijos del item a ELIMINADO#
    lista_hijo = hijos(item)
    for hijo in lista_hijo:
        hijo.estado = Relacion.ELIMINADO
        hijo.save()

    #Seteamos las relaciones de los sucesores del item a ELIMINADO#
    lista_sucesores = sucesores(item)
    for sucesor in lista_sucesores:
        sucesor.estado = Relacion.ELIMINADO
        sucesor.save()

    lista_items = Item.objects.filter(Fase=idFase).exclude(condicion=Item.ELIMINADO)
    generar_grafo_fase(idFase)
    p_consultar = usuario.tienePermisoProyecto("consulta_item", idProyecto)
    p_revivir = usuario.tienePermisoProyecto("revive_item", idProyecto)
    p_aprobar = usuario.tienePermisoProyecto("aprueba_item",idProyecto)
    p_desaprobar = usuario.tienePermisoProyecto("desaprueba_item",idProyecto)
    p_eliminar_item = usuario.tienePermisoProyecto("delete_item",idProyecto)
    p_gestionar_item = usuario.tienePermisoProyecto("change_item",idProyecto)
    p_crear_item = usuario.tienePermisoProyecto("add_item",idProyecto)
    p_solicitar_cambio = usuario.tienePermisoProyecto("solicita_item",idProyecto)
    try:
        comite = ComiteDeCambio.objects.get(Proyecto=fase.Proyecto.id)
    except ObjectDoesNotExist:
        comite = False
    items_validados = Item.objects.filter(Fase=fase).filter(Estado=Item.VALIDADO)
    if items_validados == None:
        items_validados = True
    mensaje = 'El item '+item.Nombre+' se ha eliminado exitosamente'
    suceso = True
    return render_to_response('des_fase.html',
        {'usuario_actor': usuario, 'fase': fase, 'lista_items': lista_items,
         'comite': comite, 'validados': items_validados, 'p_consultar':p_consultar, 'p_revivir':p_revivir, 'p_aprobar':p_aprobar,
         'p_desaprobar': p_desaprobar, 'p_eliminar_item':p_eliminar_item, 'p_gestionar_item':p_gestionar_item,'p_crear_item':p_crear_item,
         'p_solicitar_cambio':p_solicitar_cambio, 'mensaje': mensaje, 'suceso': suceso},
        context_instance=RequestContext(request))

def revivir_item(request, id_proyecto, id_fase):
    usuario = request.user
    fase = Fase.objects.get(pk=id_fase)
    lista_items = Item.objects.filter(Fase=fase).exclude(condicion=Item.ACTIVO)

    """
    lista_eliminados = reversion.get_deleted(Item)
    lista_items=[]

    for item in lista_eliminados:
       for key,value in item.field_dict.iteritems():
           if key == 'Fase' and value == int(id_fase):
                lista_items.append(item)
    """

    return render_to_response('item/items_eliminados.html',
        {'usuario_actor': usuario, 'fase': fase, 'lista_items': lista_items},
        context_instance=RequestContext(request))

def item_revivido(request, id_proyecto,  id_fase, id_version):

    usuario = request.user
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    fase = Fase.objects.get(pk=id_fase)
    item = Item.objects.get(pk=id_version)
    relacion = Relacion.objects.get(item=item)
    item.condicion = Item.ACTIVO
    relacion.estado = Relacion.ACTIVO
    """
    lista_eliminados = reversion.get_deleted(Item)
    item = lista_eliminados.get(id=id_version)

    id_revision = item.revision_id
    item.revert()

    lista_atributos_eliminados = reversion.get_deleted(Campo)
    for atributo in lista_atributos_eliminados:
        if atributo.revision_id == id_revision:
            atributo.revert()

    lista_relaciones_eliminadas = reversion.get_deleted(Relacion)
    try:
            relacion = lista_relaciones_eliminadas.get(revision_id=id_revision)
            relacion.revert()
    except IntegrityError:
            relacion = Relacion.objects.create(item=Item.objects.get(pk=item.object_id))
    """

    item.save()
    relacion.save()
    #Seteamos las relaciones de los hijos del item a ELIMINADO#
    lista_hijo = hijos(item)
    for hijo in lista_hijo:
        #agregar el control de ciclo
        hijo.estado = Relacion.ACTIVO
        hijo.save()

    #Seteamos las relaciones de los sucesores del item a ELIMINADO#
    lista_sucesores = sucesores(item)
    for sucesor in lista_sucesores:
        #agregar el control de ciclo
        sucesor.estado = Relacion.ACTIVO
        sucesor.save()



    suceso = True
    mensaje= 'Item revivido'
    lista_items = Item.objects.filter(Fase=id_fase).exclude(condicion=Item.ELIMINADO)
    generar_grafo_fase(id_fase)
    p_consultar = usuario.tienePermisoProyecto("consulta_item", id_proyecto)
    p_revivir = usuario.tienePermisoProyecto("revive_item", id_proyecto)
    p_aprobar = usuario.tienePermisoProyecto("aprueba_item", id_proyecto)
    p_desaprobar = usuario.tienePermisoProyecto("desaprueba_item", id_proyecto)
    p_eliminar_item = usuario.tienePermisoProyecto("delete_item", id_proyecto)
    p_gestionar_item = usuario.tienePermisoProyecto("change_item", id_proyecto)
    p_crear_item = usuario.tienePermisoProyecto("add_item", id_proyecto)
    p_solicitar_cambio = usuario.tienePermisoProyecto("solicita_item", id_proyecto)
    try:
        comite = ComiteDeCambio.objects.get(Proyecto=fase.Proyecto.id)
    except ObjectDoesNotExist:
        comite = False
    items_validados = Item.objects.filter(Fase=fase).filter(Estado=Item.VALIDADO)
    if items_validados == None:
        items_validados = True
    return render_to_response('des_fase.html',
        {'usuario_actor': usuario, 'fase': fase, 'lista_items': lista_items,
         'comite': comite, 'validados': items_validados, 'p_consultar':p_consultar, 'p_revivir':p_revivir, 'p_aprobar':p_aprobar,
         'p_desaprobar': p_desaprobar, 'p_eliminar_item':p_eliminar_item, 'p_gestionar_item':p_gestionar_item,'p_crear_item':p_crear_item,
         'p_solicitar_cambio':p_solicitar_cambio, 'mensaje': mensaje, 'suceso': suceso},
        context_instance=RequestContext(request))

def generar_grafo_proyecto(id_proyecto):
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    fases_proyecto = Fase.objects.filter(Proyecto=proyecto)
    relaciones_proyecto = []
    grafo = pydot.Dot(graph_type='digraph', rankdir="LR",labelloc='b', labeljust='r', ranksep=1)
    grafo.set_node_defaults(shape="record")
    grafo.set_edge_defaults(color="blue", arrowhead="vee", weight="1")
    for fase in fases_proyecto:
        nombreFase = fase.Nombre.replace(" ", "_")
        cluster = pydot.Cluster(graph_name=nombreFase,label=nombreFase,style='filled',color='lightgrey')
        items_fase = Item.objects.filter(Fase=fase)
        for item in items_fase:
            if item.Estado == "VAL":
                cluster.add_node(pydot.Node(name=item.Nombre, label = "<f0>%s|<f1>Costo $: %d"%(item.Nombre,item.CostoUnitario)
                                        , style="filled", fillcolor="#8AD4FF"))
            elif item.Estado == "FIN":
                cluster.add_node(pydot.Node(name=item.Nombre, label = "<f0>%s|<f1>Costo $: %d"%(item.Nombre,item.CostoUnitario)
                                        , style="filled", fillcolor="#1EED40"))
            elif item.Estado == "REV":
                cluster.add_node(pydot.Node(name=item.Nombre, label = "<f0>%s|<f1>Costo $: %d"%(item.Nombre,item.CostoUnitario)
                                        , style="filled", fillcolor="#F7F245"))
            elif item.Estado == "CRE":
                cluster.add_node(pydot.Node(name=item.Nombre, label = "<f0>%s|<f1>Costo $: %d"%(item.Nombre,item.CostoUnitario)
                                        , style="filled", fillcolor="#FC8702"))
            else:
                cluster.add_node(pydot.Node(name=item.Nombre, label = "<f0>%s|<f1>Costo $: %d"%(item.Nombre,item.CostoUnitario)
                                        , style="filled", fillcolor="white"))
            if Relacion.objects.filter(item=item):
                # r_temporal = Relacion.objects.get(item=item)
                # if r_temporal.estado == "A"
                #   relaciones_proyecto.append(r_temporal)
                relaciones_proyecto.append(Relacion.objects.get(item=item))
        grafo.add_subgraph(cluster)
    for relacion in relaciones_proyecto:
        if relacion.padre:
            grafo.add_edge(pydot.Edge(src=relacion.padre.Nombre,dst=relacion.item.Nombre,label="%d"%relacion.padre.CostoUnitario,color="blue"))
        if relacion.antecesor:
            grafo.add_edge(pydot.Edge(src=relacion.antecesor.Nombre,dst=relacion.item.Nombre,label="%d"%relacion.antecesor.CostoUnitario,color="green"))
    grafo.write_png(BASE_DIR+'/static/media/grafoProyectoActual.png')

def generar_grafo_fase(id_fase):
    fase = Fase.objects.get(pk=id_fase)
    relaciones_fase = []
    grafo = pydot.Dot(graph_type='digraph', rankdir="LR",labelloc='b', labeljust='r', ranksep=1)
    grafo.set_node_defaults(shape="component")
    grafo.set_edge_defaults(arrowhead="vee", weight="0")
    nombreFase = fase.Nombre.replace(" ", "_")
    cluster = pydot.Cluster(graph_name=nombreFase,label=nombreFase, style='filled',color='lightgrey')
    items_fase = Item.objects.filter(Fase=fase)
    for item in items_fase:
        if item.Estado == "VAL":
            cluster.add_node(pydot.Node(name=item.Nombre, style="filled", fillcolor="#8AD4FF")) # azul claro
        elif item.Estado == "FIN":
            cluster.add_node(pydot.Node(name=item.Nombre, style="filled", fillcolor="#1EED40")) # verde claro
        elif item.Estado == "REV":
            cluster.add_node(pydot.Node(name=item.Nombre, style="filled", fillcolor="#F7F245")) # amarillo claro
        elif item.Estado == "CRE":
            cluster.add_node(pydot.Node(name=item.Nombre, style="filled", fillcolor="#FC8702")) # naranja claro
        else:
            cluster.add_node(pydot.Node(name=item.Nombre, style="filled", fillcolor="white"))
        if Relacion.objects.filter(item=item):
            # r_temporal = Relacion.objects.get(item=item)
            # if r_temporal.estado == "A"
            #   relaciones_fase.append(r_temporal)
            relaciones_fase.append(Relacion.objects.get(item=item))
    grafo.add_subgraph(cluster)
    for relacion in relaciones_fase:
        if relacion.padre:
            grafo.add_edge(pydot.Edge(src=relacion.padre.Nombre,dst=relacion.item.Nombre,color="blue"))
    grafo.write_png(BASE_DIR+'/static/media/grafoFaseActual.png')

def generar_grafo_calculo_impacto_costo_unitario(id_proyecto, id_item):
    id = int(id_item)
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    fases_proyecto = Fase.objects.filter(Proyecto=proyecto)
    relaciones_proyecto = []
    grafo = pydot.Dot(graph_type='digraph', rankdir="LR",labelloc='b', labeljust='r', ranksep=1)
    grafo.set_node_defaults(shape="record")
    grafo.set_edge_defaults(color="blue", arrowhead="vee", weight="1")
    for fase in fases_proyecto:
        nombreFase = fase.Nombre.replace(" ", "_")
        cluster = pydot.Cluster(graph_name=nombreFase,label=nombreFase,style='filled',color='lightgrey')
        items_fase = Item.objects.filter(Fase=fase)
        for item in items_fase:
            if item.pk == id:
                cluster.add_node(pydot.Node(name=item.Nombre, label = "<f0>%s|<f1>Costo $: %d"%(item.Nombre,item.CostoUnitario)
                                        , style="filled", fillcolor="green"))
            else:
                cluster.add_node(pydot.Node(name=item.Nombre, label = "<f0>%s|<f1>Costo $: %d"%(item.Nombre,item.CostoUnitario)
                                        , style="filled", fillcolor="white"))
            if Relacion.objects.filter(item=item):
                # r_temporal = Relacion.objects.get(item=item)
                # if r_temporal.estado == "A"
                #   relaciones_proyecto.append(r_temporal)
                relaciones_proyecto.append(Relacion.objects.get(item=item))
        grafo.add_subgraph(cluster)
    for relacion in relaciones_proyecto:
        if relacion.padre:
            grafo.add_edge(pydot.Edge(src=relacion.padre.Nombre,dst=relacion.item.Nombre,label="%d"%relacion.padre.CostoUnitario,color="blue"))
        if relacion.antecesor:
            grafo.add_edge(pydot.Edge(src=relacion.antecesor.Nombre,dst=relacion.item.Nombre,label="%d"%relacion.antecesor.CostoUnitario,color="green"))
    grafo.write_png(BASE_DIR+'/static/media/grafoImpactoUnitario.png')

def generar_grafo_calculo_impacto_costo_temporal(id_proyecto, id_item):
    id = int(id_item)
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    fases_proyecto = Fase.objects.filter(Proyecto=proyecto)
    relaciones_proyecto = []
    grafo = pydot.Dot(graph_type='digraph', rankdir="LR",labelloc='b', labeljust='r', ranksep=1)
    grafo.set_node_defaults(shape="record")
    grafo.set_edge_defaults(color="blue", arrowhead="vee", weight="1")
    for fase in fases_proyecto:
        nombreFase = fase.Nombre.replace(" ", "_")
        cluster = pydot.Cluster(graph_name=nombreFase,label=nombreFase,style='filled',color='lightgrey')
        items_fase = Item.objects.filter(Fase=fase)
        for item in items_fase:
            if item.pk == id:
                cluster.add_node(pydot.Node(name=item.Nombre, label = "<f0>%s|<f1>C. Temporal: %d"%(item.Nombre, item.CostoTemporal)
                                        , style="filled", fillcolor="green"))
            else:
                cluster.add_node(pydot.Node(name=item.Nombre, label = "<f0>%s|<f1>C. Temporal: %d"%(item.Nombre, item.CostoTemporal)
                                        , style="filled", fillcolor="white"))
            if Relacion.objects.filter(item=item):
                # r_temporal = Relacion.objects.get(item=item)
                # if r_temporal.estado == "A"
                #   relaciones_proyecto.append(r_temporal)
                relaciones_proyecto.append(Relacion.objects.get(item=item))
        grafo.add_subgraph(cluster)
    for relacion in relaciones_proyecto:
        if relacion.padre:
            grafo.add_edge(pydot.Edge(src=relacion.padre.Nombre,dst=relacion.item.Nombre,label="%d"%relacion.padre.CostoTemporal,color="blue"))
        if relacion.antecesor:
            grafo.add_edge(pydot.Edge(src=relacion.antecesor.Nombre,dst=relacion.item.Nombre,label="%d"%relacion.antecesor.CostoTemporal,color="green"))
    grafo.write_png(BASE_DIR+'/static/media/grafoImpactoTemporal.png')


def historial_item(request, id_proyecto, id_fase, id_item):
    item = Item.objects.get(pk=id_item)
    usuario = request.user
    lista_versiones = reversion.get_for_object(item)
    p_reversionar_item = usuario.tienePermisoProyecto("reversiona_item",id_proyecto)
    return render_to_response('item/historial_item.html', {'lista_versiones': lista_versiones, 'item':item,
                                                                            'proyecto':Proyecto.objects.get(pk=id_proyecto),
                                                                            'fase': Fase.objects.get(pk=id_fase), 'p_reversionar_item':p_reversionar_item},
                              context_instance=RequestContext(request))

def reversion_item(request, id_proyecto,  id_fase, id_item, id_version):
    item = Item.objects.get(pk=id_item)
    version_antigua = item.Version
    fase = Fase.objects.get(pk=id_fase)
    usuario = request.user
    mensaje = 'Se ha reversionado el item '+str(item.Nombre)
    relacion = Relacion.objects.get(item=item)
    lista_atributos = Campo.objects.filter(item=item)
    lista_items = Item.objects.filter(Fase=id_fase)
    version = item.Version
    id_version = int('0'+id_version)
    version_item = 0

    lista_version = reversion.get_for_object(item)

    for version in lista_version:
        if version.id == id_version:
            version_item = version.revision_id
            version.revert()

    for atributo in lista_atributos:
        lista_version = reversion.get_for_object(atributo)
        for version in lista_version:
            if version.revision_id == version_item:
                version.revert()

    lista_version = reversion.get_for_object(relacion)
    for version in lista_version:
        if version.revision_id == version_item:
            version.revert()

    item = Item.objects.get(pk=id_item)
    item.Version = version_antigua+1
    item.save()
    generar_grafo_fase(id_fase)
    suceso = True
    p_consultar = usuario.tienePermisoProyecto("consulta_item", id_proyecto)
    p_revivir = usuario.tienePermisoProyecto("revive_item", id_proyecto)
    p_aprobar = usuario.tienePermisoProyecto("aprueba_item", id_proyecto)
    p_desaprobar = usuario.tienePermisoProyecto("desaprueba_item", id_proyecto)
    p_eliminar_item = usuario.tienePermisoProyecto("delete_item", id_proyecto)
    p_gestionar_item = usuario.tienePermisoProyecto("change_item", id_proyecto)
    p_crear_item = usuario.tienePermisoProyecto("add_item", id_proyecto)
    p_solicitar_cambio = usuario.tienePermisoProyecto("solicita_item", id_proyecto)
    try:
        comite = ComiteDeCambio.objects.get(Proyecto=fase.Proyecto.id)
    except ObjectDoesNotExist:
        comite = False
    items_validados = Item.objects.filter(Fase=fase).filter(Estado=Item.VALIDADO)
    if items_validados == None:
        items_validados = True
    return render_to_response('des_fase.html',
        {'usuario_actor': usuario, 'fase': fase, 'lista_items': lista_items,
         'comite': comite, 'validados': items_validados, 'p_consultar':p_consultar, 'p_revivir':p_revivir, 'p_aprobar':p_aprobar,
         'p_desaprobar': p_desaprobar, 'p_eliminar_item':p_eliminar_item, 'p_gestionar_item':p_gestionar_item,'p_crear_item':p_crear_item,
         'p_solicitar_cambio':p_solicitar_cambio, 'mensaje': mensaje, 'suceso': suceso},
        context_instance=RequestContext(request)
    )


def detalle_item_version(request, idProyecto, idFase, idItem, idVersion):
    usuario = request.user
    fase = Fase.objects.get(pk=idFase)
    item = Item.objects.get(pk=idItem)
    relacion = Relacion.objects.get(item=item)

    lista_version_item = reversion.get_for_object(item)
    lista_version_relacion = reversion.get_for_object(relacion)
    lista_atributos = Campo.objects.filter(item=item)

    idn_version = int('0'+idVersion)
    revision_id = 0
    campos = []
    item_version = 0
    relacion_version = 0

    for version in lista_version_item:
        if version.id == idn_version:
            item_version = version
            revision_id = version.revision_id

    for atributo in lista_atributos:
        lista_version = reversion.get_for_object(atributo)
        for version in lista_version:
            if version.revision_id == revision_id:
                campos.append(version)

    for version in lista_version_relacion:
        if version.revision_id == revision_id:
            relacion_version = version


    return render_to_response(
        'item/detalle_version.html',
        {'usuario_actor': usuario, 'item': item, 'campo_version': campos,'fase':fase, 'item_version':item_version, 'relacion_version':relacion_version,'campos': lista_atributos, 'relacion': relacion},
        context_instance=RequestContext(request)
    )



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
        'relacion/gestion_relaciones.html',
        {'usuario_actor': usuario, 'relacion': relacion, 'item': item, 'fase': fase,
         'hijos': lista_hijos, 'sucesores': lista_sucesores},
        context_instance=RequestContext(request)
    )

@reversion.create_revision()
def asignar_padre_view(request, id_proyecto, id_fase, id_item):
    usuario = request.user
    item = Item.objects.get(pk=id_item)
    fase = Fase.objects.get(pk=id_fase)
    relacion = Relacion.objects.get(item=item)
    relacion.estado = Relacion.ACTIVO

    lista_items = Item.objects.filter(Fase=fase).exclude(pk=id_item).exclude(condicion=Item.ELIMINADO)
    if request.method=='POST':
        formulario = PadreForm(request.POST, instance=relacion)
        if formulario.is_valid():
            if generaCiclo(id_item, request.POST['padre']):
                suceso = False
                mensaje = 'Error: Esta relacion genera un ciclo'
            else:
                formulario.save()
                mensaje = 'Padre asignado exitosamente'
                suceso = True

            item.Version += 1
            item.save()
            for campo in Campo.objects.filter(item=item):
                    campo.save()
            generar_grafo_fase(id_fase)
            return render_to_response(
                'relacion/gestion_relaciones.html',
                {'usuario': usuario, 'fase': fase, 'mensaje': mensaje, 'suceso': suceso, 'item': item,
                 'relacion': relacion},
                context_instance=RequestContext(request)
            )
    else:
        formulario = PadreForm()
    return render_to_response(
        'relacion/asignar_padre.html',
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
    relacion = Relacion.objects.get(item=item)

    if fase.Numero != 1:
        faseAnterior = Fase.objects.get(Proyecto=proyecto, Numero=fase.Numero-1)
        lista_items = Item.objects.filter(Fase=faseAnterior).filter(Estado=Item.VALIDADO)

    if request.method=='POST':
        formulario = AntecesorForm(request.POST, instance=relacion)
        if formulario.is_valid():
            formulario.save()

        item.Version += 1
        item.save()
        for campo in Campo.objects.filter(item=item):
            campo.save()

        mensaje = 'Antecesor asignado exitosamente'
        suceso = True
        relacion = Relacion.objects.get(item=item)
        generar_grafo_fase(id_fase)
        return render_to_response(
                'relacion/gestion_relaciones.html',
                {'usuario':usuario, 'fase':fase, 'mensaje':mensaje, 'suceso':suceso, 'item': item, 'relacion': relacion},
                context_instance=RequestContext(request)
            )
    else:
        formulario = AntecesorForm()

    return render_to_response(
        'relacion/asignar_antecesor.html',
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
        'archivo/gestion_archivos.html',
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
                'archivo/gestion_archivos.html',
                {'usuario_actor':usuario, 'fase':fase, 'mensaje':mensaje, 'suceso':suceso,
                 'item': item, 'lista_archivos': lista_archivos},
                context_instance=RequestContext(request)
            )
    else:
        formulario = ArchivoForm()
    return render_to_response(
        'archivo/agregar_archivo.html',
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
    return render_to_response('detalle_fase.html',
                              {'usuario_actor': usuario_actor, 'fase': fase, 'proyecto':proyecto},
                              context_instance=RequestContext(request))

def detalle_proyecto(request, id_proyecto):
    usuario_actor = request.user
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    return render_to_response('detalle_proyecto_des.html', {'usuario_actor': usuario_actor, 'proyecto': proyecto},
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
    costo_monetario_total = costo_m_atras + costo_m_adelante + item.CostoUnitario
    costo_t_atras = costo_temporal_atras(item)
    costo_t_adelante = costo_temporal_adelante(item)
    costo_temporal_total = costo_t_atras + costo_t_adelante + item.CostoTemporal
    generar_grafo_calculo_impacto_costo_temporal(id_proyecto,id_item)
    generar_grafo_calculo_impacto_costo_unitario(id_proyecto,id_item)
    return render_to_response(
        'item/impacto.html',
        {'fase': fase, 'usuario': usuario, 'item': item, 'costo_monetario_atras': costo_m_atras,
         'costo_monetario_adelante': costo_m_adelante, 'costo_temporal_atras': costo_t_atras,
         'costo_temporal_adelante': costo_t_adelante, 'costo_monetario_total': costo_monetario_total,
         'costo_temporal_total': costo_temporal_total},
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
        'relacion/eliminar.html',
        {'usuario': usuario, 'fase': fase, 'item': item},
        context_instance=RequestContext(request)
    )

def relacion_eliminada_view(request, id_proyecto, id_fase, id_item):
    usuario = request.user
    fase = Fase.objects.get(pk=id_fase)
    item = Item.objects.get(pk=id_item)
    relacion = Relacion.objects.get(item=item)
    relacion.padre = None
    relacion.antecesor = None
    relacion.save()
    suceso = True
    mensaje = 'Relacion eliminada con exito'
    generar_grafo_fase(id_fase)
    return render_to_response(
        'relacion/gestion_relaciones.html',
        {'usuario': usuario, 'fase': fase, 'item': item, 'suceso': suceso, 'mensaje': mensaje, 'relacion': relacion},
        context_instance=RequestContext(request)
    )

def aprobar_item_view(request, id_proyecto, id_fase, id_item):
    usuario = request.user
    fase = Fase.objects.get(pk=id_fase)
    item = Item.objects.get(pk=id_item)
    relacion = Relacion.objects.get(item=item)
    lista_items = Item.objects.filter(Fase=fase)
    if relacion.padre != None:
        print relacion.padre.Estado
        if relacion.padre.Estado != Item.VALIDADO and relacion.padre.Estado != Item.FINALIZADO:
            suceso = False
            mensaje = 'El item no puede ser aprobado ya que su padre todavia no ha sido aprobado'
            p_consultar = usuario.tienePermisoProyecto("consulta_item", id_proyecto)
            p_revivir = usuario.tienePermisoProyecto("revive_item", id_proyecto)
            p_aprobar = usuario.tienePermisoProyecto("aprueba_item", id_proyecto)
            p_desaprobar = usuario.tienePermisoProyecto("desaprueba_item", id_proyecto)
            p_eliminar_item = usuario.tienePermisoProyecto("delete_item", id_proyecto)
            p_gestionar_item = usuario.tienePermisoProyecto("change_item", id_proyecto)
            p_crear_item = usuario.tienePermisoProyecto("add_item", id_proyecto)
            p_solicitar_cambio = usuario.tienePermisoProyecto("solicita_item", id_proyecto)
            try:
                comite = ComiteDeCambio.objects.get(Proyecto=fase.Proyecto.id)
            except ObjectDoesNotExist:
                comite = False
            items_validados = Item.objects.filter(Fase=fase).filter(Estado=Item.VALIDADO)
            if items_validados == None:
                items_validados = True
            return render_to_response('des_fase.html',
                {'usuario_actor': usuario, 'fase': fase, 'lista_items': lista_items,
                 'comite': comite, 'validados': items_validados, 'p_consultar':p_consultar, 'p_revivir':p_revivir, 'p_aprobar':p_aprobar,
                 'p_desaprobar': p_desaprobar, 'p_eliminar_item':p_eliminar_item, 'p_gestionar_item':p_gestionar_item,'p_crear_item':p_crear_item,
                 'p_solicitar_cambio':p_solicitar_cambio, 'mensaje': mensaje, 'suceso': suceso},
                context_instance=RequestContext(request)
            )
    if fase.Numero != 1:
        if posee_antecesor(item) == False:
            suceso = False
            mensaje = 'El item no posee antecesor directo ni indirecto, por lo tanto no puede ser aprobado'
            p_consultar = usuario.tienePermisoProyecto("consulta_item", id_proyecto)
            p_revivir = usuario.tienePermisoProyecto("revive_item", id_proyecto)
            p_aprobar = usuario.tienePermisoProyecto("aprueba_item", id_proyecto)
            p_desaprobar = usuario.tienePermisoProyecto("desaprueba_item", id_proyecto)
            p_eliminar_item = usuario.tienePermisoProyecto("delete_item", id_proyecto)
            p_gestionar_item = usuario.tienePermisoProyecto("change_item", id_proyecto)
            p_crear_item = usuario.tienePermisoProyecto("add_item", id_proyecto)
            p_solicitar_cambio = usuario.tienePermisoProyecto("solicita_item", id_proyecto)
            try:
                comite = ComiteDeCambio.objects.get(Proyecto=fase.Proyecto.id)
            except ObjectDoesNotExist:
                comite = False
            items_validados = Item.objects.filter(Fase=fase).filter(Estado=Item.VALIDADO)
            if items_validados == None:
                items_validados = True
            return render_to_response('des_fase.html',
                {'usuario_actor': usuario, 'fase': fase, 'lista_items': lista_items,
                 'comite': comite, 'validados': items_validados, 'p_consultar':p_consultar, 'p_revivir':p_revivir, 'p_aprobar':p_aprobar,
                 'p_desaprobar': p_desaprobar, 'p_eliminar_item':p_eliminar_item, 'p_gestionar_item':p_gestionar_item,'p_crear_item':p_crear_item,
                 'p_solicitar_cambio':p_solicitar_cambio, 'mensaje': mensaje, 'suceso': suceso},
                context_instance=RequestContext(request))
    return render_to_response(
        'item/finalizar.html',
        {'usuario': usuario, 'fase': fase, 'item': item},
        context_instance=RequestContext(request))



def item_finalizado_view(request, id_proyecto, id_fase, id_item):
    usuario = request.user
    fase = Fase.objects.get(pk=id_fase)
    item = Item.objects.get(pk=id_item)

    item.Estado = item.FINALIZADO
    item.save()
    suceso = True
    mensaje = 'Item aprobado exitosamente'
    lista_items = Item.objects.filter(Fase=fase)
    generar_grafo_fase(id_fase)
    p_consultar = usuario.tienePermisoProyecto("consulta_item", id_proyecto)
    p_revivir = usuario.tienePermisoProyecto("revive_item", id_proyecto)
    p_aprobar = usuario.tienePermisoProyecto("aprueba_item", id_proyecto)
    p_desaprobar = usuario.tienePermisoProyecto("desaprueba_item", id_proyecto)
    p_eliminar_item = usuario.tienePermisoProyecto("delete_item", id_proyecto)
    p_gestionar_item = usuario.tienePermisoProyecto("change_item", id_proyecto)
    p_crear_item = usuario.tienePermisoProyecto("add_item", id_proyecto)
    p_solicitar_cambio = usuario.tienePermisoProyecto("solicita_item", id_proyecto)
    try:
        comite = ComiteDeCambio.objects.get(Proyecto=fase.Proyecto.id)
    except ObjectDoesNotExist:
        comite = False
    items_validados = Item.objects.filter(Fase=fase).filter(Estado=Item.VALIDADO)
    if items_validados == None:
        items_validados = True
    return render_to_response('des_fase.html',
        {'usuario_actor': usuario, 'fase': fase, 'lista_items': lista_items,
         'comite': comite, 'validados': items_validados, 'p_consultar':p_consultar, 'p_revivir':p_revivir, 'p_aprobar':p_aprobar,
         'p_desaprobar': p_desaprobar, 'p_eliminar_item':p_eliminar_item, 'p_gestionar_item':p_gestionar_item,'p_crear_item':p_crear_item,
         'p_solicitar_cambio':p_solicitar_cambio, 'mensaje': mensaje, 'suceso': suceso},
        context_instance=RequestContext(request))




def solicitud_crear_view(request, id_proyecto, id_fase):
    usuario = request.user
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    fase = Fase.objects.get(pk=id_fase)
    lista_items = Item.objects.filter(Fase=fase)
    lista_items = lista_items.filter(Estado=Item.VALIDADO)
    solicitud = SolicitudCambio(proyecto=proyecto, fase=fase, usuario=usuario)
    if request.method == 'POST':
        formulario = SolicitudCambioForm(request.POST, instance=solicitud)
        formulario.fields["items"].queryset = lista_items
        formulario.fields["items"].help_text = "Haga doble click en el item que desee agregar"
        if formulario.is_valid():
            formulario.save()
            solicitud = SolicitudCambio.objects.last()
            for item in solicitud.items.all():
                item.Estado = Item.SOLICITUD
                item.save()
            lista_items = Item.objects.filter(Fase=fase)
            suceso = True
            mensaje = "Solicitud de cambio creada exitosamente"
            comite = ComiteDeCambio.objects.get(Proyecto=proyecto)
            for miembro in comite.Miembros.all():
                voto = Voto()
                voto.solicitud = solicitud
                voto.usuario = miembro
                voto.save()
            p_consultar = usuario.tienePermisoProyecto("consulta_item", id_proyecto)
            p_revivir = usuario.tienePermisoProyecto("revive_item", id_proyecto)
            p_aprobar = usuario.tienePermisoProyecto("aprueba_item", id_proyecto)
            p_desaprobar = usuario.tienePermisoProyecto("desaprueba_item", id_proyecto)
            p_eliminar_item = usuario.tienePermisoProyecto("delete_item", id_proyecto)
            p_gestionar_item = usuario.tienePermisoProyecto("change_item", id_proyecto)
            p_crear_item = usuario.tienePermisoProyecto("add_item", id_proyecto)
            p_solicitar_cambio = usuario.tienePermisoProyecto("solicita_item", id_proyecto)
            try:
                comite = ComiteDeCambio.objects.get(Proyecto=fase.Proyecto.id)
            except ObjectDoesNotExist:
                comite = False
            items_validados = Item.objects.filter(Fase=fase).filter(Estado=Item.VALIDADO)
            if items_validados == None:
                items_validados = True
            return render_to_response('des_fase.html',
                {'usuario_actor': usuario, 'fase': fase, 'lista_items': lista_items,
                 'comite': comite, 'validados': items_validados, 'p_consultar':p_consultar, 'p_revivir':p_revivir, 'p_aprobar':p_aprobar,
                 'p_desaprobar': p_desaprobar, 'p_eliminar_item':p_eliminar_item, 'p_gestionar_item':p_gestionar_item,'p_crear_item':p_crear_item,
                 'p_solicitar_cambio':p_solicitar_cambio, 'mensaje': mensaje, 'suceso': suceso},
                context_instance=RequestContext(request))

    else:
        formulario = SolicitudCambioForm(instance=solicitud)
        formulario.fields["items"].queryset = lista_items
        formulario.fields["items"].help_text = "Haga doble click en el item que desee agregar"
    return render_to_response(
        'solicitud.html',
        {'formulario':formulario,'usuario_actor':usuario, 'fase':fase},
        context_instance=RequestContext(request)
    )

def desaprobar_view(request, id_proyecto, id_fase, id_item):
    usuario = request.user
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    fase = Fase.objects.get(pk=id_fase)
    item = Item.objects.get(pk=id_item)
    return render_to_response(
        'item/desaprobar.html',
        {'usuario_actor': usuario, 'fase': fase, 'item': item},
        context_instance=RequestContext(request)
    )

def desaprobado_view(request, id_proyecto, id_fase, id_item):
    usuario = request.user
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    fase = Fase.objects.get(pk=id_fase)
    item = Item.objects.get(pk=id_item)
    item.Estado = item.CONSTRUCCION
    item.save()
    suceso = True
    mensaje = 'Item desaprobado exitosamente'
    lista_items = Item.objects.filter(Fase=fase)
    generar_grafo_fase(id_fase)
    p_consultar = usuario.tienePermisoProyecto("consulta_item", id_proyecto)
    p_revivir = usuario.tienePermisoProyecto("revive_item", id_proyecto)
    p_aprobar = usuario.tienePermisoProyecto("aprueba_item", id_proyecto)
    p_desaprobar = usuario.tienePermisoProyecto("desaprueba_item", id_proyecto)
    p_eliminar_item = usuario.tienePermisoProyecto("delete_item", id_proyecto)
    p_gestionar_item = usuario.tienePermisoProyecto("change_item", id_proyecto)
    p_crear_item = usuario.tienePermisoProyecto("add_item", id_proyecto)
    p_solicitar_cambio = usuario.tienePermisoProyecto("solicita_item", id_proyecto)
    try:
        comite = ComiteDeCambio.objects.get(Proyecto=fase.Proyecto.id)
    except ObjectDoesNotExist:
        comite = False
    items_validados = Item.objects.filter(Fase=fase).filter(Estado=Item.VALIDADO)
    if items_validados == None:
        items_validados = True
    return render_to_response('des_fase.html',
        {'usuario_actor': usuario, 'fase': fase, 'lista_items': lista_items,
         'comite': comite, 'validados': items_validados, 'p_consultar':p_consultar, 'p_revivir':p_revivir, 'p_aprobar':p_aprobar,
         'p_desaprobar': p_desaprobar, 'p_eliminar_item':p_eliminar_item, 'p_gestionar_item':p_gestionar_item,'p_crear_item':p_crear_item,
         'p_solicitar_cambio':p_solicitar_cambio, 'mensaje': mensaje, 'suceso': suceso},
        context_instance=RequestContext(request))


def solicitudes_de_cambio_view(request, id_proyecto, id_fase):
    usuario = request.user
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    fase  = Fase.objects.get(pk=id_fase)
    solicitudes = SolicitudCambio.objects.filter(usuario=usuario)
    return render_to_response('solicitudes.html', {'usuario_actor':usuario, 'proyecto':proyecto, 'fase':fase,'solicitudes':solicitudes},
        context_instance=RequestContext(request))

def detalle_solicitud(request, id_proyecto, id_fase, id_solicitud):
    usuario = request.user
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    fase  = Fase.objects.get(pk=id_fase)
    solicitud = SolicitudCambio.objects.get(pk=id_solicitud)
    lista_item = solicitud.items
    return render_to_response('detalle_solicitud_des.html',{'usuario_actor':usuario, 'proyecto':proyecto, 'fase':fase,'solicitud':solicitud, 'lista_item':lista_item}
                              ,context_instance=RequestContext(request))

def posee_antecesor(item):
    relacion = Relacion.objects.get(item=item)
    if relacion.antecesor != None:
        return True
    while relacion != False:
        if relacion.antecesor != None:
            return True
        try:
            relacion = Relacion.objects.get(item=relacion.padre)
        except ObjectDoesNotExist:
            relacion = False
    return False

def revisar_item_vista(request, id_proyecto, id_fase, id_item):

    usuario = request.user
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    fase = Fase.objects.get(pk=id_fase)
    item = Item.objects.get(pk=id_item)
    campos = Campo.objects.filter(item=item)
    relacion = Relacion.objects.get(item=item)
    lista_hijos = hijos(item)
    lista_sucesores = sucesores(item)
    if relacion.padre.Estado != Item.VALIDADO:
        suceso = False
        mensaje = 'No se puede revisar el item porque el padre aun no se ha modificado'
        lista_items = Item.objects.filter(Fase=fase)
        p_consultar = usuario.tienePermisoProyecto("consulta_item", id_proyecto)
        p_revivir = usuario.tienePermisoProyecto("revive_item", id_proyecto)
        p_aprobar = usuario.tienePermisoProyecto("aprueba_item", id_proyecto)
        p_desaprobar = usuario.tienePermisoProyecto("desaprueba_item", id_proyecto)
        p_eliminar_item = usuario.tienePermisoProyecto("delete_item", id_proyecto)
        p_gestionar_item = usuario.tienePermisoProyecto("change_item", id_proyecto)
        p_crear_item = usuario.tienePermisoProyecto("add_item", id_proyecto)
        p_solicitar_cambio = usuario.tienePermisoProyecto("solicita_item", id_proyecto)
        try:
            comite = ComiteDeCambio.objects.get(Proyecto=fase.Proyecto.id)
        except ObjectDoesNotExist:
            comite = False
        items_validados = Item.objects.filter(Fase=fase).filter(Estado=Item.VALIDADO)
        if items_validados == None:
            items_validados = True
        return render_to_response('des_fase.html',
            {'usuario_actor': usuario, 'fase': fase, 'lista_items': lista_items,
             'comite': comite, 'validados': items_validados, 'p_consultar':p_consultar, 'p_revivir':p_revivir, 'p_aprobar':p_aprobar,
             'p_desaprobar': p_desaprobar, 'p_eliminar_item':p_eliminar_item, 'p_gestionar_item':p_gestionar_item,'p_crear_item':p_crear_item,
             'p_solicitar_cambio':p_solicitar_cambio, 'mensaje': mensaje, 'suceso': suceso},
            context_instance=RequestContext(request))
    solicitudes = SolicitudCambio.objects.filter(usuario=usuario, estado=SolicitudCambio.ACEPTADA, fase=fase)
    boolean = False
    for solicitud in solicitudes:
        if solicitud.items.all().filter(pk=relacion.padre.id):
            boolean = True

    if boolean == False:
        suceso = False
        mensaje = 'Usted no posee permiso para modificar este item'
        lista_items = Item.objects.filter(Fase=fase)
        return render_to_response(
            'des_fase.html',
            {'usuario_actor': usuario, 'fase': fase, 'lista_items': lista_items,
             'mensaje': mensaje, 'suceso': suceso},
            context_instance=RequestContext(request)
        )

    return render_to_response(
        'item/revisar.html',
        {'usuario_actor': usuario, 'item': item, 'campos': campos, 'fase':fase, 'relacion': relacion,
         'hijos': lista_hijos, 'sucesores': lista_sucesores},
        context_instance=RequestContext(request)
    )

def item_revisado_vista(request, id_proyecto, id_fase, id_item):
    usuario = request.user
    fase = Fase.objects.get(pk=id_fase)
    item = Item.objects.get(pk=id_item)
    lista_version = reversion.get_for_object(item)
    version_Revisado = lista_version.first()
    for version in lista_version:
        if version.revision_id < version_Revisado.revision_id:
            version.revert()
            break

    suceso = True
    mensaje = 'El item ha sido revisado'
    lista_items = Item.objects.filter(Fase=fase)
    p_consultar = usuario.tienePermisoProyecto("consulta_item", id_proyecto)
    p_revivir = usuario.tienePermisoProyecto("revive_item", id_proyecto)
    p_aprobar = usuario.tienePermisoProyecto("aprueba_item", id_proyecto)
    p_desaprobar = usuario.tienePermisoProyecto("desaprueba_item", id_proyecto)
    p_eliminar_item = usuario.tienePermisoProyecto("delete_item", id_proyecto)
    p_gestionar_item = usuario.tienePermisoProyecto("change_item", id_proyecto)
    p_crear_item = usuario.tienePermisoProyecto("add_item", id_proyecto)
    p_solicitar_cambio = usuario.tienePermisoProyecto("solicita_item", id_proyecto)
    try:
        comite = ComiteDeCambio.objects.get(Proyecto=fase.Proyecto.id)
    except ObjectDoesNotExist:
        comite = False
    items_validados = Item.objects.filter(Fase=fase).filter(Estado=Item.VALIDADO)
    if items_validados == None:
        items_validados = True
    return render_to_response('des_fase.html',
        {'usuario_actor': usuario, 'fase': fase, 'lista_items': lista_items,
         'comite': comite, 'validados': items_validados, 'p_consultar':p_consultar, 'p_revivir':p_revivir, 'p_aprobar':p_aprobar,
         'p_desaprobar': p_desaprobar, 'p_eliminar_item':p_eliminar_item, 'p_gestionar_item':p_gestionar_item,'p_crear_item':p_crear_item,
         'p_solicitar_cambio':p_solicitar_cambio, 'mensaje': mensaje, 'suceso': suceso},
        context_instance=RequestContext(request))

