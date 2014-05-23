from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.contrib.auth.views import SetPasswordForm
from django.conf import settings



admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'SGP.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),


    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'sesion.views.iniciar_sesion'),
    url(r'^ingresar/$', 'sesion.views.iniciar_sesion'),
    url(r'^cerrar/$', 'sesion.views.cerrar_sesion'),
    url(r'^administracion/$', 'administracion.views.administracion'),
    url(r'^usuario/$', 'sesion.views.gestion_usuario'),
    url(r'^usuario/password/$', 'django.contrib.auth.views.password_change',
        {'current_app': 'administracion',
         'template_name': 'gestion_usuario.html',
         'post_change_redirect': 'pass_done',
         'password_change_form': SetPasswordForm},
        name='password'),
    url(r'^usuario/password/done$', 'django.contrib.auth.views.password_change_done',
        {'template_name': 'gestion_exito_pass.html'}, name='pass_done'),
    url(r'^$', include('django.contrib.auth.urls')),
############################################URL USUARIO#################################################################
    url(r'^administracion/usuarios/$', 'administracion.views.administrar_usuario'),
    url(r'^administracion/usuarios/nuevo/$', 'administracion.views.crear_usuario'),
    url(r'^administracion/usuarios/modificar/(?P<id_usuario_p>\d+)/password/$', 'administracion.views.pass_change'),
    url(r'^administracion/usuarios/cambio_de_estado/(?P<id_usuario_p>\d+)/$', 'administracion.views.cambioEstado_usuario_form'),
    url(r'^administracion/usuarios/detalle/(?P<id_usuario_p>\d+)/$', 'administracion.views.detalle_usuario'),

###############################################URL PROYECTO#############################################################
    url(r'^administracion/proyectos/$', 'administracion.views.administrar_proyecto'),
    url(r'^administracion/proyectos/nuevo/$', 'administracion.views.nuevo_proyecto'),
    url(r'^administracion/proyectos/(?P<id_proyecto>\d+)/detalle/$', 'administracion.views.detalle_proyecto'),
    url(r'^administracion/proyectos/(?P<id_proyecto>\d+)/iniciar/$', 'administracion.views.confirmar_iniciar_proyecto'),
    url(r'^administracion/proyectos/(?P<id_proyecto>\d+)/iniciado/$', 'administracion.views.iniciar_proyecto'),
    url(r'^administracion/proyectos/(?P<id_proyecto>\d+)/modificar/$', 'administracion.views.modificar_proyecto'),
    url(r'^administracion/proyectos/(?P<id_proyecto>\d+)/completar/$', 'administracion.views.modificar_proyecto_lider'),
    url(r'^administracion/proyectos/(?P<id_proyecto>\d+)/usuarios/$', 'administracion.views.proyecto_asignar_usuarios'),
    url(r'^administracion/proyectos/(?P<id_proyecto>\d+)/eliminar/$', 'administracion.views.confirmar_eliminar_proyecto'),
    url(r'^administracion/proyectos/(?P<id_proyecto>\d+)/eliminado/$', 'administracion.views.eliminar_proyecto'),

################################################URL FASE################################################################
    url(r'^administracion/proyectos/(?P<id_proyecto>\d+)/fases/$', 'administracion.views.administrar_fases'),
    url(r'^administracion/proyectos/fases/subir/(?P<id_fase>\d+)/$', 'administracion.views.ordenar_fase_subir'),
    url(r'^administracion/proyectos/fases/bajar/(?P<id_fase>\d+)/$', 'administracion.views.ordenar_fase_bajar'),
    url(r'^administracion/proyectos/(?P<id_proyecto>\d+)/fases/nuevo/$', 'administracion.views.crear_fase'),
    url(r'^administracion/proyectos/(?P<id_proyecto>\d+)/fases/(?P<idFase>\d+)/detalle/$', 'administracion.views.detalle_fase'),
    url(r'^administracion/proyectos/(?P<id_proyecto>\d+)/fases/(?P<idFase>\d+)/modificar/$', 'administracion.views.modificar_fase'),
    url(r'^administracion/proyectos/(?P<id_proyecto>\d+)/fases/(?P<idFase>\d+)/usuarios/$', 'administracion.views.fase_asignar_usuarios'),
    url(r'^administracion/proyectos/(?P<id_proyecto>\d+)/fases/(?P<idFase>\d+)/eliminar/$', 'administracion.views.confirmar_eliminar_fase'),
    url(r'^administracion/proyectos/(?P<id_proyecto>\d+)/fases/(?P<idFase>\d+)/eliminado/$', 'administracion.views.eliminar_fase'),

################################################URL ROL#################################################################
    url(r'^administracion/roles/$', 'administracion.views.administrar_roles'),
    url(r'^administracion/roles/nuevo/$', 'administracion.views.crear_rol'),
    url(r'^administracion/roles/asignar/(?P<id_usuario>\d+)/$', 'administracion.views.asignar_rol'),
    url(r'^administracion/roles/listar/$', 'administracion.views.listar_roles'),
    url(r'^administracion/roles/listar/(?P<idRol>\d+)/detalle/$', 'administracion.views.detalle_rol'),
    url(r'^administracion/roles/listar/(?P<idRol>\d+)/modificar/$', 'administracion.views.modificar_rol'),
    url(r'^administracion/roles/listar/(?P<idRol>\d+)/eliminar/$', 'administracion.views.confirmar_eliminar_rol'),
    url(r'^administracion/roles/listar/(?P<idRol>\d+)/eliminado/$', 'administracion.views.eliminar_rol'),

###############################################URL CREDENCIAL###########################################################
    url(r'^administracion/credenciales/$', 'administracion.views.administrar_credencial'),
################################################URL ATRIBUTO############################################################
    url(r'^administracion/proyectos/(?P<id_proyecto>\d+)/fases/(?P<id_fase>\d+)/atributos/$', 'administracion.views.administrar_atributo'),
    url(r'^administracion/proyectos/(?P<id_proyecto>\d+)/fases/(?P<id_fase>\d+)/atributos/nuevo/$', 'administracion.views.crear_atributo'),
    url(r'^administracion/proyectos/(?P<id_proyecto>\d+)/fases/(?P<id_fase>\d+)/atributos/detalle/(?P<id_atributo>\d+)/$', 'administracion.views.detalle_atributo'),
    url(r'^administracion/proyectos/(?P<id_proyecto>\d+)/fases/(?P<id_fase>\d+)/atributos/modificar/(?P<id_atributo>\d+)/$', 'administracion.views.modificar_atributo'),
    url(r'^administracion/proyectos/(?P<id_proyecto>\d+)/fases/(?P<id_fase>\d+)/atributos/eliminar/(?P<id_atributo>\d+)/$', 'administracion.views.confirmar_eliminar_atributo'),
    url(r'^administracion/proyectos/(?P<id_proyecto>\d+)/fases/(?P<id_fase>\d+)/atributos/eliminado/(?P<id_atributo>\d+)/$', 'administracion.views.eliminar_atributo'),

###############################################URL TIPO DE ITEM#########################################################
    url(r'^administracion/proyectos/(?P<id_proyecto>\d+)/fases/(?P<id_fase>\d+)/tipos/$', 'administracion.views.administrar_tipoItem'),
    url(r'^administracion/proyectos/(?P<id_proyecto>\d+)/fases/(?P<id_fase>\d+)/tipos/nuevo/$', 'administracion.views.crear_tipoItem'),
    url(r'^administracion/proyectos/(?P<id_proyecto>\d+)/fases/(?P<id_fase>\d+)/tipos/detalle/(?P<id_tipo>\d+)/$', 'administracion.views.detalle_tipoItem'),
    url(r'^administracion/proyectos/(?P<id_proyecto>\d+)/fases/(?P<id_fase>\d+)/tipos/modificar/(?P<id_tipo>\d+)/$', 'administracion.views.modificar_tipo'),
    url(r'^administracion/proyectos/(?P<id_proyecto>\d+)/fases/(?P<id_fase>\d+)/tipos/eliminar/(?P<id_tipo>\d+)/$', 'administracion.views.confirmar_eliminar_tipo'),
    url(r'^administracion/proyectos/(?P<id_proyecto>\d+)/fases/(?P<id_fase>\d+)/tipos/eliminado/(?P<id_tipo>\d+)/$', 'administracion.views.eliminar_tipo'),
    url(r'^administracion/proyectos/(?P<id_proyecto>\d+)/fases/(?P<id_fase>\d+)/tipos/importar$', 'administracion.views.importar_tipo'),


###############################################URL DESARROLLO###########################################################
    url(r'^desarrollo/$', 'desarrollo.views.desarrollo'),
    url(r'^desarrollo/proyecto/(?P<id_proyecto>\d+)/$', 'desarrollo.views.des_proyecto'),

    url(r'^desarrollo/proyecto/(?P<id_proyecto>\d+)/fase/(?P<id_fase>\d+)/$', 'desarrollo.views.des_fase'),
    url(r'^desarrollo/proyecto/(?P<id_proyecto>\d+)/fase/(?P<id_fase>\d+)/detalle/$', 'desarrollo.views.detalle_fase'),



    url(r'^desarrollo/proyecto/(?P<id_proyecto>\d+)/fase/(?P<id_fase>\d+)/crear_item/$', 'desarrollo.views.crear_item'),
    url(r'^desarrollo/proyecto/(?P<id_proyecto>\d+)/fase/(?P<id_fase>\d+)/item/(?P<id_item>\d+)/modificar/$', 'desarrollo.views.mod_item'),
    url(r'^desarrollo/proyecto/(?P<idProyecto>\d+)/fase/(?P<idFase>\d+)/item/(?P<idItem>\d+)/eliminar/$', 'desarrollo.views.conf_eliminar_item'),
    url(r'^desarrollo/proyecto/(?P<idProyecto>\d+)/fase/(?P<idFase>\d+)/item/(?P<idItem>\d+)/eliminado/$', 'desarrollo.views.eliminar_item'),
    url(r'^desarrollo/proyecto/(?P<id_proyecto>\d+)/fase/(?P<id_fase>\d+)/item/(?P<id_item>\d+)/completar/$', 'desarrollo.views.completar_item'),
    url(r'^desarrollo/proyecto/(?P<idProyecto>\d+)/fase/(?P<idFase>\d+)/item/(?P<idItem>\d+)/detalle/$', 'desarrollo.views.detalle_item_vista'),

    url(r'^desarrollo/proyecto/(?P<id_proyecto>\d+)/fase/(?P<id_fase>\d+)/item/(?P<id_item>\d+)/relaciones/$', 'desarrollo.views.gestion_relacion_view'),
    url(r'^desarrollo/proyecto/(?P<id_proyecto>\d+)/fase/(?P<id_fase>\d+)/item/(?P<id_item>\d+)/relaciones/asignar/padre/$', 'desarrollo.views.asignar_padre_view'),
    url(r'^desarrollo/proyecto/(?P<id_proyecto>\d+)/fase/(?P<id_fase>\d+)/item/(?P<id_item>\d+)/relaciones/asignar/antecesor/$', 'desarrollo.views.asignar_antecesor_view'),
    url(r'^desarrollo/proyecto/(?P<id_proyecto>\d+)/fase/(?P<id_fase>\d+)/item/(?P<id_item>\d+)/relaciones/eliminar/$', 'desarrollo.views.eliminar_relacion_view'),
    url(r'^desarrollo/proyecto/(?P<id_proyecto>\d+)/fase/(?P<id_fase>\d+)/item/(?P<id_item>\d+)/relaciones/eliminada/$', 'desarrollo.views.relacion_eliminada_view'),

    url(r'^desarrollo/proyecto/(?P<id_proyecto>\d+)/fase/(?P<id_fase>\d+)/item/(?P<id_item>\d+)/archivos/$', 'desarrollo.views.gestion_archivos_view'),
    url(r'^desarrollo/proyecto/(?P<id_proyecto>\d+)/fase/(?P<id_fase>\d+)/item/(?P<id_item>\d+)/relaciones/agregar/$', 'desarrollo.views.agregar_archivo_view'),

    url(r'^desarrollo/proyecto/(?P<id_proyecto>\d+)/fase/(?P<id_fase>\d+)/item/(?P<id_item>\d+)/versiones/$', 'desarrollo.views.historial_item'),
    url(r'^desarrollo/proyecto/(?P<id_proyecto>\d+)/fase/(?P<id_fase>\d+)/item/(?P<id_item>\d+)/versiones/(?P<id_version>\d+)/$', 'desarrollo.views.reversion_item'),
    url(r'^desarrollo/proyecto/(?P<idProyecto>\d+)/fase/(?P<idFase>\d+)/item/(?P<idItem>\d+)/versiones/(?P<idVersion>\d+)/detalle/$', 'desarrollo.views.detalle_item_version'),


    url(r'^desarrollo/proyecto/(?P<id_proyecto>\d+)/fase/(?P<id_fase>\d+)/eliminados/$', 'desarrollo.views.revivir_item'),
    url(r'^desarrollo/proyecto/(?P<id_proyecto>\d+)/fase/(?P<id_fase>\d+)versiones/(?P<id_version>\d+)/$', 'desarrollo.views.item_revivido'),

    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, }),
    url(r'^desarrollo/proyecto/(?P<id_proyecto>\d+)/fase/(?P<id_fase>\d+)/item/(?P<id_item>\d+)/impacto/$', 'desarrollo.views.impacto_view'),

    url(r'^desarrollo/proyecto/(?P<id_proyecto>\d+)/fase/(?P<id_fase>\d+)/item/(?P<id_item>\d+)/aprobar/$', 'desarrollo.views.finalizar_item_view'),
    url(r'^desarrollo/proyecto/(?P<id_proyecto>\d+)/fase/(?P<id_fase>\d+)/item/(?P<id_item>\d+)/aprobado/$', 'desarrollo.views.item_finalizado_view'),
    url(r'^desarrollo/proyecto/(?P<id_proyecto>\d+)/fase/(?P<id_fase>\d+)/item/(?P<id_item>\d+)/desaprobar/$', 'desarrollo.views.desaprobar_view'),
    url(r'^desarrollo/proyecto/(?P<id_proyecto>\d+)/fase/(?P<id_fase>\d+)/item/(?P<id_item>\d+)/desaprobado/$', 'desarrollo.views.desaprobado_view'),

    url(r'^desarrollo/proyecto/(?P<id_proyecto>\d+)/fase/(?P<id_fase>\d+)/solicitud/cambio/$', 'desarrollo.views.solicitud_cambio_view'),


########################################################################################################################
#####################################URL GESTION DE CAMBIOS#############################################################
########################################################################################################################
    url(r'^gestion/$', 'gestion.views.gestion'),
    url(r'^gestion/proyecto/(?P<id_proyecto>\d+)/$', 'gestion.views.gestion_proyecto'),
    url(r'^gestion/proyecto/(?P<id_proyecto>\d+)/comite/$', 'gestion.views.gestion_comite'),
    url(r'^gestion/proyecto/(?P<id_proyecto>\d+)/comite/nuevo/$', 'gestion.views.crear_comite'),
    url(r'^gestion/proyecto/(?P<id_proyecto>\d+)/fase/(?P<id_fase>\d+)/$', 'gestion.views.gestion_fase'),
    url(r'^gestion/proyecto/(?P<id_proyecto>\d+)/fase/(?P<id_fase>\d+)/lineaBase$', 'gestion.views.crear_lineaBase_view'),

)

