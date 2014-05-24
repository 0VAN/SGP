from django.shortcuts import render_to_response, RequestContext, get_object_or_404
from django.contrib.auth.decorators import login_required
from gestion.models import *
from gestion.forms import *
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
    return render_to_response('gestion.html', {'lista_proyectos': lista_proyectos, 'usuario_actor': usuario},
                              context_instance=RequestContext(request))
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
    lista_lineaBase = LineBase.objects.filter(Fase=fase)
    return render_to_response('gestion_fase.html',
        {'usuario_actor': usuario, 'fase': fase, 'lista_lineabase': lista_lineaBase},
        context_instance=RequestContext(request))

def gestion_comite(request, id_proyecto):
    usuario = request.user
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    comite = False
    if tiene_comite(id_proyecto):
        comite = ComiteDeCambio.objects.get(Proyecto=proyecto)
    return render_to_response('comite/gestion_comite.html',
        {'usuario_actor': usuario, 'proyecto':proyecto, 'comite':comite},
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
    comite = ComiteDeCambio(Usuario1=usuario, Proyecto=proyecto)
    if request.method == 'POST':
        formulario = ComiteForm(request.POST, instance=comite)
        formulario.fields["Usuario2"].queryset = proyecto.Usuarios.all()
        formulario.fields["Usuario3"].queryset = proyecto.Usuarios.all()
        if formulario.is_valid():
            rolComite = Group.objects.get(name="Integrante de Comite")
            formulario.save()
            usuario.groups.add(rolComite)
            usuario.save()
            usuario2 = User.objects.get(pk=request.POST["Usuario2"])
            usuario2.groups.add(rolComite)
            usuario2.save()
            usuario3 = User.objects.get(pk=request.POST["Usuario3"])
            usuario3.groups.add(rolComite)
            usuario3.save()
            return render_to_response('comite/gestion_comite.html',
        {'usuario_actor': usuario, 'proyecto': proyecto, 'comite': comite},
        context_instance=RequestContext(request))
        else:
            return render_to_response('comite/crear_comite.html',{'formulario':formulario,'usuario_actor': usuario,
                                                              'id_proyecto':id_proyecto},
        context_instance=RequestContext(request))

    else:
        formulario = ComiteForm(instance=comite)
        formulario.fields["Usuario2"].queryset = proyecto.Usuarios.all()
        formulario.fields["Usuario3"].queryset = proyecto.Usuarios.all()
        return render_to_response('comite/crear_comite.html',{'formulario':formulario,'usuario_actor': usuario,
                                                              'id_proyecto':id_proyecto},
        context_instance=RequestContext(request))


def crear_lineaBase_view(request, id_proyecto, id_fase):
    usuario = request.user
    fase = Fase.objects.get(pk=id_fase)
    lista_lineaBase = LineBase.objects.filter(Fase=fase)
    lista_items = Item.objects.filter(Fase=fase)
    lista_items = lista_items.filter(Estado=Item.FINALIZADO)
    lineabase = LineBase(Fase=fase, Usuario=usuario)
    if request.method == 'POST':
        formulario = LineBaseForm(request.POST, instance=lineabase)
        formulario.fields["Items"].queryset = lista_items
        formulario.fields["Items"].help_text = "Haga doble click en el item que desee agregar"
        if formulario.is_valid():
            formulario.save()
            lineabase = LineBase.objects.last()
            for item in lineabase.Items.all():
                item.Estado = item.VALIDADO
                item.save()
            return render_to_response(
                'gestion_fase.html',
                {'usuario_actor': usuario, 'fase': fase, 'lista_lineabase': lista_lineaBase},
                context_instance=RequestContext(request)
            )

    else:
        formulario = LineBaseForm(instance=lineabase)
        formulario.fields["Items"].queryset = lista_items
        formulario.fields["Items"].help_text = "Haga doble click en el item que desee agregar"
    return render_to_response(
        'lineaBase_form.html',
        {'formulario':formulario,'usuario_actor':usuario, 'fase':fase},
        context_instance=RequestContext(request)
    )


def solicitudes_view(request, id_proyecto):
    usuario = request.user
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    comite = ComiteDeCambio.objects.get(Proyecto=proyecto)
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
    votos_aceptados = 0
    votos_rechazados = 0

    voto1 = Voto.objects.get(usuario=comite.Usuario1, solicitud=solicitud)
    if voto1.estado == Voto.ACEPTADO:
        votos_aceptados += 1
    elif voto1.estado == Voto.RECHAZADO:
        votos_rechazados += 1

    voto2 = Voto.objects.get(usuario=comite.Usuario2, solicitud=solicitud)
    if voto2.estado == Voto.ACEPTADO:
        votos_aceptados += 1
    elif voto2.estado == Voto.RECHAZADO:
        votos_rechazados += 1

    voto3 = Voto.objects.get(usuario=comite.Usuario3, solicitud=solicitud)
    if voto3.estado == Voto.ACEPTADO:
        votos_aceptados += 1
    elif voto3.estado == Voto.RECHAZADO:
        votos_rechazados += 1

    voto = Voto.objects.get(usuario=usuario, solicitud=solicitud)
    return render_to_response(
        'solicitud/detalle_solicitud.html',
        {'usuario_actor':usuario, 'proyecto':proyecto, 'solicitud':solicitud,
         'voto':voto, 'votos_aceptados': votos_aceptados, 'votos_rechazados': votos_rechazados},
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
    votos_aceptados = 0
    votos_rechazados = 0

    voto1 = Voto.objects.get(usuario=comite.Usuario1, solicitud=solicitud)
    if voto1.estado == Voto.ACEPTADO:
        votos_aceptados += 1
    elif voto1.estado == Voto.RECHAZADO:
        votos_rechazados += 1

    voto2 = Voto.objects.get(usuario=comite.Usuario2, solicitud=solicitud)
    if voto2.estado == Voto.ACEPTADO:
        votos_aceptados += 1
    elif voto2.estado == Voto.RECHAZADO:
        votos_rechazados += 1

    voto3 = Voto.objects.get(usuario=comite.Usuario3, solicitud=solicitud)
    if voto3.estado == Voto.ACEPTADO:
        votos_aceptados += 1
    elif voto3.estado == Voto.RECHAZADO:
        votos_rechazados += 1

    total_votos = votos_aceptados + votos_rechazados
    if total_votos == 3:
        if votos_aceptados > votos_rechazados:
            solicitud.estado = SolicitudCambio.ACEPTADA
        else:
            solicitud.estado = SolicitudCambio.RECHAZADA
        solicitud.save()
    return render_to_response(
        'solicitud/detalle_solicitud.html',
        {'usuario_actor':usuario, 'proyecto':proyecto, 'solicitud':solicitud, 'voto':voto,
         'votos_aceptados': votos_aceptados, 'votos_rechazados': votos_rechazados},
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
    votos_aceptados = 0
    votos_rechazados = 0

    voto1 = Voto.objects.get(usuario=comite.Usuario1, solicitud=solicitud)
    if voto1.estado == Voto.ACEPTADO:
        votos_aceptados += 1
    elif voto1.estado == Voto.RECHAZADO:
        votos_rechazados += 1

    voto2 = Voto.objects.get(usuario=comite.Usuario2, solicitud=solicitud)
    if voto2.estado == Voto.ACEPTADO:
        votos_aceptados += 1
    elif voto2.estado == Voto.RECHAZADO:
        votos_rechazados += 1

    voto3 = Voto.objects.get(usuario=comite.Usuario3, solicitud=solicitud)
    if voto3.estado == Voto.ACEPTADO:
        votos_aceptados += 1
    elif voto3.estado == Voto.RECHAZADO:
        votos_rechazados += 1

    total_votos = votos_aceptados + votos_rechazados
    if total_votos == 3:
        if votos_aceptados > votos_rechazados:
            solicitud.estado = SolicitudCambio.ACEPTADA
        else:
            solicitud.estado = SolicitudCambio.RECHAZADA
        solicitud.save()
    return render_to_response(
        'solicitud/detalle_solicitud.html',
        {'usuario_actor':usuario, 'proyecto':proyecto, 'solicitud':solicitud, 'voto':voto,
         'votos_aceptados': votos_aceptados, 'votos_rechazados': votos_rechazados},
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
                item.Estado = Item.REVISION
                item.save()
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
