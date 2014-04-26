from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.contrib.auth.views import SetPasswordForm
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
    url(r'^administracion/usuarios/modificar/(?P<id_usuario_p>\d+)/$', 'administracion.views.modificar_usuario'),
    url(r'^administracion/usuarios/modificar/(?P<id_usuario_p>\d+)/password/$', 'administracion.views.pass_change'),
    url(r'^administracion/usuarios/cambio_de_estado/(?P<id_usuario_p>\d+)/$', 'administracion.views.cambioEstado_usuario_form'),
    url(r'^administracion/usuarios/detalle/(?P<id_usuario_p>\d+)/$', 'administracion.views.detalle_usuario'),

###############################################URL PROYECTO#############################################################
    url(r'^administracion/proyectos/$', 'administracion.views.administrar_proyecto'),
    url(r'^administracion/proyectos/nuevo/$', 'administracion.views.nuevo_proyecto'),
    url(r'^administracion/proyectos/(?P<id_proyecto>\d+)/detalle/$', 'administracion.views.detalle_proyecto'),
    url(r'^administracion/proyectos/(?P<id_proyecto>\d+)/iniciar/$', 'administracion.views.iniciar_proyecto'),

################################################URL FASE################################################################
    url(r'^administracion/proyectos/(?P<id_proyecto>\d+)/fases/$', 'administracion.views.administrar_fases'),
    url(r'^administracion/proyectos/(?P<id_proyecto>\d+)/fases/nuevo/$', 'administracion.views.crear_fase'),
    url(r'^administracion/proyectos/(?P<id_proyecto>\d+)/fases/detalle/(?P<idFase>\d+)/$', 'administracion.views.detalle_fase'),
    url(r'^administracion/proyectos/(?P<id_proyecto>\d+)/fases/(?P<idFase>\d+)/modificar/$', 'administracion.views.modificar_fase'),
    url(r'^administracion/proyectos/(?P<id_proyecto>\d+)/fases/(?P<idFase>\d+)/eliminar/$', 'administracion.views.vista_eliminar_fase'),
    url(r'^administracion/proyectos/(?P<id_proyecto>\d+)/fases/(?P<idFase>\d+)/eliminado/$', 'administracion.views.eliminar_fase'),

################################################URL ROL#################################################################
    url(r'^administracion/roles/$', 'administracion.views.administrar_roles'),
    url(r'^administracion/roles/nuevo/$', 'administracion.views.crear_rol'),
    url(r'^administracion/roles/asignar/(?P<id_rol>\d+)/$', 'administracion.views.asignar_rol'),
    url(r'^administracion/roles/detalle/(?P<idRol>\d+)/$', 'administracion.views.detalle_rol'),
    url(r'^administracion/roles/(?P<idRol>\d+)/modificar/$', 'administracion.views.modificar_rol'),
    url(r'^administracion/roles/(?P<idRol>\d+)/eliminar/$', 'administracion.views.vista_eliminar_rol'),
    url(r'^administracion/roles/(?P<idRol>\d+)/eliminado/$', 'administracion.views.eliminar_rol'),

###############################################URL CREDENCIAL###########################################################
    url(r'^administracion/credenciales/$', 'administracion.views.administrar_credencial'),
################################################URL ATRIBUTO############################################################

    url(r'^administracion/proyectos/(?P<id_proyecto>\d+)/atributos/$', 'administracion.views.administrar_atributo'),
    url(r'^administracion/proyectos/(?P<id_proyecto>\d+)/atributos/nuevo/$', 'administracion.views.crear_atributo'),
    url(r'^administracion/proyectos/(?P<id_proyecto>\d+)/atributos/detalle/(?P<id_atributo>\d+)/$', 'administracion.views.detalle_atributo'),
    url(r'^administracion/proyectos/(?P<id_proyecto>\d+)/atributos/modificar/(?P<id_atributo>\d+)/$', 'administracion.views.modificar_atributo'),
    url(r'^administracion/proyectos/(?P<id_proyecto>\d+)/atributos/eliminar/(?P<id_atributo>\d+)/$', 'administracion.views.eliminar_atributo'),
###############################################URL DESARROLLO###########################################################
    url(r'^desarrollo/$', 'desarrollo.views.desarrollo'),
    url(r'^desarrollo/proyecto/(?P<id_proyecto>\d+)/$', 'desarrollo.views.des_proyecto'),
    url(r'^desarrollo/proyecto/(?P<id_proyecto>\d+)/fase/(?P<id_fase>\d+)/$', 'desarrollo.views.des_fase'),
)

