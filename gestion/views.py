from django.shortcuts import render_to_response, RequestContext, get_object_or_404
from django.contrib.auth.decorators import login_required
from gestion.models import *
from desarrollo.models import *
from gestion.forms import *
from desarrollo.models import *
from django.contrib.auth.models import Group
# Create your views here.
@login_required(login_url='/iniciar_sesion')
def gestion(request):
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
    return render_to_response(
        'gestion.html',
        {'lista_proyectos': lista_proyectos, 'usuario_actor': usuario},
        context_instance=RequestContext(request)
    )
def gestion_proyecto(request, id_proyecto):
    usuario = request.user
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    lista_fases = Fase.objects.filter(Proyecto=id_proyecto)
    return render_to_response('gestion_proyecto.html',
        {'usuario_actor': usuario, 'proyecto': proyecto, 'lista_fases': lista_fases},
        context_instance=RequestContext(request))

def gestion_fase(request, id_proyecto, id_fase):
    usuario = request.user
    fase = Fase.objects.get(pk=id_fase)
    lista_lineaBase = LineaBase.objects.filter(Fase=fase)
    return render_to_response('gestion_fase.html',
        {'usuario_actor': usuario, 'fase': fase, 'lista_lineabase': lista_lineaBase},
        context_instance=RequestContext(request))

def gestion_comite(request, id_proyecto):
    usuario = request.user
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    comite = False
    miembros = None
    if tiene_comite(id_proyecto):
        comite = ComiteDeCambio.objects.get(Proyecto=proyecto)
        miembros = comite.Miembros.all()
    print miembros
    return render_to_response('comite/gestion_comite.html',
        {'usuario_actor': usuario, 'proyecto':proyecto, 'comite':comite, 'miembros': miembros},
        context_instance=RequestContext(request))

def tiene_comite(id_proyecto):
    try:
        proyecto = Proyecto.objects.get(pk=id_proyecto)
        comite = ComiteDeCambio.objects.filter(Proyecto=proyecto)
        if comite:
            return True
        return False
    except:
        return False

def crear_comite(request, id_proyecto):
    usuario = request.user
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    comite_instancia = ComiteDeCambio(Proyecto=proyecto)

    if request.method == 'POST':
        formulario = ComiteForm(request.POST, instance=comite_instancia)
        formulario.fields["Miembros"].queryset = proyecto.Usuarios.all()
        if formulario.is_valid():
            print 'paso'
            rolComite = Group.objects.get(name="Integrante de Comite")
            comite = formulario.save()
            cantidad = comite.Miembros.all().count()
            print cantidad % 2
            if (cantidad % 2) != 0:
                print 'entro'
                suceso = False
                mensaje = 'El comite debe tener un numero impar de miembros'
                comite.delete()
                formulario = ComiteForm(instance=comite_instancia)
                formulario.fields["Miembros"].queryset = proyecto.Usuarios.all()
                return render_to_response(
                    'comite/crear_comite.html',
                    {'formulario':formulario, 'usuario_actor': usuario, 'id_proyecto': id_proyecto,
                     'suceso': suceso, 'mensaje': mensaje},
                    context_instance=RequestContext(request)
                )
            comite.Miembros.add(usuario)

            for user in comite.Miembros.all():
                user.groups.add(rolComite)
                user.save()

            comite.save()
            miembros = comite.Miembros.all()
            return render_to_response(
                'comite/gestion_comite.html',
                {'usuario_actor': usuario, 'proyecto': proyecto, 'comite': comite, 'miembros': miembros},
                context_instance=RequestContext(request)
            )
        else:
            return render_to_response(
                'comite/crear_comite.html',
                {'formulario':formulario,'usuario_actor': usuario, 'id_proyecto': id_proyecto},
                context_instance=RequestContext(request)
            )

    else:
        formulario = ComiteForm(instance=comite_instancia)
        formulario.fields["Miembros"].queryset = proyecto.Usuarios.all()
        return render_to_response(
            'comite/crear_comite.html',
            {'formulario':formulario,'usuario_actor': usuario, 'id_proyecto':id_proyecto},
            context_instance=RequestContext(request)
        )


def crear_lineaBase_view(request, id_proyecto, id_fase):
    usuario = request.user
    fase = Fase.objects.get(pk=id_fase)
    lista_lineaBase = LineaBase.objects.filter(Fase=fase)
    lista_items = Item.objects.filter(Fase=fase)
    lista_items = lista_items.filter(Estado=Item.FINALIZADO)
    lineabase = LineaBase(Fase=fase, Usuario=usuario)
    if request.method == 'POST':
        formulario = LineaBaseForm(request.POST, instance=lineabase)
        formulario.fields["Items"].queryset = lista_items
        formulario.fields["Items"].help_text = "Haga doble click en el item que desee agregar"
        if formulario.is_valid():
            formulario.save()
            lineabase = LineaBase.objects.last()
            for item in lineabase.Items.all():
                item.Estado = item.VALIDADO
                item.save()
            return render_to_response(
                'gestion_fase.html',
                {'usuario_actor': usuario, 'fase': fase, 'lista_lineabase': lista_lineaBase},
                context_instance=RequestContext(request)
            )

    else:
        formulario = LineaBaseForm(instance=lineabase)
        formulario.fields["Items"].queryset = lista_items
        formulario.fields["Items"].help_text = "Haga doble click en el item que desee agregar"
    return render_to_response(
        'lineaBase_form.html',
        {'formulario':formulario,'usuario_actor':usuario, 'fase':fase},
        context_instance=RequestContext(request)
    )
def detalle_lineaBase(request, id_proyecto, id_fase, id_lineaB):
    """

    :param request:
    :param id_proyecto:
    :return:

    Vista detalle de proyecto

    | Recibe un request y un id de proyecto y retorna una pagina web detalle_proyecto.html con los detalles
    | de un proyecto

    * Variables
        -   usuario_actor: es el usuario que realiza la accion
        -   proyecto: es el proyecto que sera visualizado en detalle
    """
    usuario_actor = request.user
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    fase = Fase.objects.get(pk=id_fase)
    lineaBase =LineaBase.objects.get(pk=id_lineaB)
    lista_items = lineaBase.Items.all()
    return render_to_response('lineaBase_detalle.html', {'usuario_actor': usuario_actor, 'proyecto': proyecto,'fase':fase,
                                                         'lineaBase':lineaBase, 'lista_item':lista_items},
                              context_instance=RequestContext(request))

def solicitudes_view(request, id_proyecto):
    usuario = request.user
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    if tiene_comite(id_proyecto):
        comite = ComiteDeCambio.objects.get(Proyecto=proyecto)
    else:
        lista_proyectos = Proyecto.objects.all()
        suceso = False
        mensaje = 'Primero debe crear un comite de cambio'
        return render_to_response(
            'gestion.html',
            {'lista_proyectos': lista_proyectos, 'usuario_actor': usuario, 'suceso': suceso, 'mensaje': mensaje},
            context_instance=RequestContext(request)
        )
    lista_solicitudes = SolicitudCambio.objects.filter(proyecto=proyecto)
    return render_to_response(
        'solicitud/solicitudes.html',
        {'usuario_actor':usuario, 'proyecto':proyecto, 'lista_solicitudes': lista_solicitudes},
        context_instance=RequestContext(request)
    )

def detalle_solicitud_view(request, id_proyecto, id_solicitud):
    usuario = request.user
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    solicitud = SolicitudCambio.objects.get(pk=id_solicitud)
    comite = ComiteDeCambio.objects.get(Proyecto=proyecto)
    votos = Voto.objects.filter(solicitud=solicitud)
    votos_aceptados = 0
    votos_rechazados = 0
    votos_restantes = 0
    for voto in votos:
        if voto.estado == voto.ACEPTADO:
            votos_aceptados+=1
        elif voto.estado == voto.RECHAZADO:
            votos_rechazados+=1
        elif voto.estado == voto.PROCESO:
            votos_restantes+=1

    voto = Voto.objects.get(usuario=usuario, solicitud=solicitud)
    return render_to_response(
        'solicitud/detalle_solicitud.html',
        {'usuario_actor':usuario, 'proyecto':proyecto, 'solicitud':solicitud,
         'voto':voto, 'votos_aceptados': votos_aceptados, 'votos_rechazados': votos_rechazados,
         'votos_restantes': votos_restantes},
        context_instance=RequestContext(request)
    )


def aprobar_solicitud_view(request, id_proyecto, id_solicitud):
    usuario = request.user
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    solicitud = SolicitudCambio.objects.get(pk=id_solicitud)
    comite = ComiteDeCambio.objects.get(Proyecto=proyecto)
    voto = Voto.objects.get(usuario=usuario, solicitud=solicitud)
    voto.estado = Voto.ACEPTADO
    voto.save()
    suceso = True
    mensaje = 'Voto aprobado'
    votos = Voto.objects.filter(solicitud=solicitud)
    votos_aceptados = 0
    votos_rechazados = 0
    votos_restantes = 0
    for voto in votos:
        if voto.estado == voto.ACEPTADO:
            votos_aceptados+=1
        elif voto.estado == voto.RECHAZADO:
            votos_rechazados+=1
        elif voto.estado == voto.PROCESO:
            votos_restantes+=1


    if votos_restantes == 0:
        if votos_aceptados > votos_rechazados:
            solicitud.estado = SolicitudCambio.ACEPTADA
        else:
            solicitud.estado = SolicitudCambio.RECHAZADA
        solicitud.save()
    return render_to_response(
        'solicitud/detalle_solicitud.html',
        {'usuario_actor':usuario, 'proyecto':proyecto, 'solicitud':solicitud, 'voto':voto,
         'votos_aceptados': votos_aceptados, 'votos_rechazados': votos_rechazados, 'votos_restantes': votos_restantes},
        context_instance=RequestContext(request)
    )


def desaprobar_solicitud_view(request, id_proyecto, id_solicitud):
    usuario = request.user
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    solicitud = SolicitudCambio.objects.get(pk=id_solicitud)
    comite = ComiteDeCambio.objects.get(Proyecto=proyecto)
    voto = Voto.objects.get(usuario=usuario, solicitud=solicitud)
    voto.estado = Voto.RECHAZADO
    voto.save()
    suceso = True
    mensaje = 'Voto desaprobado'
    votos = Voto.objects.filter(solicitud=solicitud)
    votos_aceptados = 0
    votos_rechazados = 0
    votos_restantes = 0
    for voto in votos:
        if voto.estado == voto.ACEPTADO:
            votos_aceptados+=1
        elif voto.estado == voto.RECHAZADO:
            votos_rechazados+=1
        elif voto.estado == voto.PROCESO:
            votos_restantes+=1


    if votos_restantes == 0:
        if votos_aceptados > votos_rechazados:
            solicitud.estado = SolicitudCambio.ACEPTADA
        else:
            solicitud.estado = SolicitudCambio.RECHAZADA
        solicitud.save()
    return render_to_response(
        'solicitud/detalle_solicitud.html',
        {'usuario_actor':usuario, 'proyecto':proyecto, 'solicitud':solicitud, 'voto':voto,
         'votos_aceptados': votos_aceptados, 'votos_rechazados': votos_rechazados, 'votos_restantes': votos_restantes},
        context_instance=RequestContext(request)
    )


def credencial_view(request, id_proyecto, id_solicitud):
    usuario = request.user
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    solicitud = SolicitudCambio.objects.get(pk=id_solicitud)
    credencial = Credencial()
    credencial.solicitud = solicitud
    if request.method == 'POST':
        formulario = CredencialForm(request.POST, instance=credencial)
        if formulario.is_valid():
            formulario.save()
            lista_solicitudes = SolicitudCambio.objects.filter(proyecto=proyecto)
            for item in solicitud.items.all():
                item.Estado = Item.CREDENCIAL
                item.save()
                relaciones = Relacion.objects.filter(padre=item)
                for relacion in relaciones:
                    relacion.item.Estado = Item.REVISION
                    relacion.item.save()


            return render_to_response(
                'solicitud/solicitudes.html',
                {'usuario_actor':usuario, 'proyecto':proyecto, 'lista_solicitudes': lista_solicitudes},
                context_instance=RequestContext(request)
            )
    else:
        formulario = CredencialForm()
    return render_to_response(
        'solicitud/credencial.html',
        {'formulario': formulario, 'usuario_actor': usuario, 'solicitud': solicitud,
         'proyecto': proyecto},
        context_instance=RequestContext(request)
    )

def detalle_item_validados(request, id_proyecto, id_fase, id_lineaB, id_item):
    usuario = request.user
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    fase = Fase.objects.get(pk=id_fase)
    item = Item.objects.get(pk=id_item)
    campos = Campo.objects.filter(item=item)
    relacion = Relacion.objects.get(item=item)

    return render_to_response(
        'detalle_item.html',
        {'usuario_actor': usuario, 'item': item, 'campos': campos, 'fase':fase, 'relacion': relacion},   context_instance=RequestContext(request)
    )



def detalle_fase(request, id_proyecto, id_fase):
    """

    :param request:
    :param idFase:
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
    lista_item = Item.objects.filter(Fase=fase)
    return render_to_response('detalle_fase_gc.html',
                              {'usuario_actor': usuario_actor, 'fase': fase, 'proyecto':proyecto, 'lista_item':lista_item},
                              context_instance=RequestContext(request))

def detalle_item(request, id_proyecto, id_fase, id_item):
    usuario = request.user
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    fase = Fase.objects.get(pk=id_fase)
    item = Item.objects.get(pk=id_item)
    campos = Campo.objects.filter(item=item)
    relacion = Relacion.objects.get(item=item)

    return render_to_response(
        'detalle_item.html',
        {'usuario_actor': usuario, 'item': item, 'campos': campos, 'fase':fase, 'relacion': relacion},   context_instance=RequestContext(request)
    )
