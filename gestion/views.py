from django.shortcuts import render_to_response, RequestContext, get_object_or_404
from django.contrib.auth.decorators import login_required
from gestion.models import *
from gestion.forms import *
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
        formulario.fields["Usuario2"].help_text = "Seleccione el usuario para el comite"
        formulario.fields["Usuario3"].queryset = proyecto.Usuarios.all()
        formulario.fields["Usuario3"].help_text = "Seleccione el usuario para el comite"
        if formulario.is_valid():
            formulario.save()
            return render_to_response('comite/gestion_comite.html',
        {'usuario_actor': usuario, 'proyecto': proyecto, 'comite': comite},
        context_instance=RequestContext(request))

    else:
        formulario = ComiteForm(instance=comite)
        formulario.fields["Usuario2"].queryset = proyecto.Usuarios.all()
        formulario.fields["Usuario2"].label = "Integrante 2:"
        formulario.fields["Usuario3"].queryset = proyecto.Usuarios.all()
        formulario.fields["Usuario3"].label = "Integrante 3:"
        return render_to_response('comite/crear_comite.html',{'formulario':formulario,'usuario_actor': usuario,
                                                              'id_proyecto':id_proyecto},
        context_instance=RequestContext(request))


def crear_lineaBase_view(request, id_proyecto, id_fase):
    usuario = request.user
    fase = Fase.objects.get(pk=id_fase)
    lista_lineaBase = LineBase.objects.filter(Fase=fase)
    lista_items = Item.objects.filter(Fase=fase)
    lista_items = lista_items.filter(Estado='FIN')
    lineabase = LineBase(Fase=fase, Usuario=usuario)
    if request.method == 'POST':
        formulario = LineBaseForm(request.POST, instance=lineabase)
        formulario.fields["Items"].queryset = lista_items
        formulario.fields["Items"].help_text = "Haga doble click en el item que desee agregar"
        if formulario.is_valid():
            formulario.save()
            return render_to_response('gestion_fase.html',
        {'usuario_actor': usuario, 'fase': fase, 'lista_lineabase': lista_lineaBase},
        context_instance=RequestContext(request))

    else:
        formulario = LineBaseForm(instance=lineabase)
        formulario.fields["Items"].queryset = lista_items
        formulario.fields["Items"].help_text = "Haga doble click en el item que desee agregar"
        return render_to_response('lineaBase_form.html',{'formulario':formulario,'usuario_actor':usuario,
                                                         'fase':fase},
        context_instance=RequestContext(request))