from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.contrib.auth.views import SetPasswordForm
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'SGP.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),


    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'administracion.views.iniciar_sesion'),
    url(r'^ingresar/$', 'administracion.views.iniciar_sesion'),
    url(r'^cerrar/$', 'administracion.views.cerrar_sesion'),
    url(r'^administracion/$', 'administracion.views.administracion'),

############################################URL USUARIO#################################################################
    url(r'^administracion/usuarios/$', 'administracion.views.administrar_usuario'),
    url(r'^administracion/usuarios/nuevo/$', 'administracion.views.crear_usuario'),
    url(r'^administracion/usuarios/modificar/$', 'administracion.views.modificar_usuario'),
    url(r'^administracion/usuarios/modificar/password/$', 'django.contrib.auth.views.password_change',
        {'current_app': 'administracion',
         'template_name': 'usuario/form_usuario.html',
         'post_change_redirect': 'pass_done',
         'password_change_form': SetPasswordForm},
        name='password'),
    url(r'^administracion/usuarios/modificar/password/done$', 'django.contrib.auth.views.password_change_done',
        {'template_name': 'usuario/operacion_usuario_exito_pass.html'}, name='pass_done'),
    url(r'^administracion/usuarios/modificar/', include('django.contrib.auth.urls')),

    url(r'^administracion/usuarios/cambio_de_estado/(?P<id_usuario_p>\d+)$', 'administracion.views.cambioEstado_usuario_form'),
    url(r'^administracion/usuarios/detalle/(?P<id_usuario_p>\d+)$', 'administracion.views.detalle_usuario'),

###############################################URL PROYECTO#############################################################
    url(r'^administracion/proyectos/$', 'administracion.views.administrar_proyecto'),
    url(r'^administracion/proyectos/nuevo$', 'administracion.views.nuevo_proyecto'),
    url(r'^administracion/proyectos/detalle/(?P<id_proyecto>\d+)$', 'administracion.views.detalle_proyecto'),

################################################URL FASE################################################################
    url(r'^administracion/proyectos/(?P<id_proyecto>\d+)/fases/$', 'administracion.views.administrar_fases'),
    url(r'^administracion/proyectos/(?P<id_proyecto>\d+)/fases/nuevo/$', 'administracion.views.crear_fase'),
    url(r'^administracion/proyectos/(?P<id_proyecto>\d+)/fases/detalle/(?P<idFase>\d+)$', 'administracion.views.detalle_fase'),
    url(r'^administracion/proyectos/(?P<id_proyecto>\d+)/fases/(?P<idFase>\d+)/modificar/$', 'administracion.views.modificar_fase'),
    url(r'^administracion/proyectos/(?P<id_proyecto>\d+)/fases/(?P<idFase>\d+)/eliminar/$', 'administracion.views.vista_eliminar_fase'),
    url(r'^administracion/proyectos/(?P<id_proyecto>\d+)/fases/(?P<idFase>\d+)/eliminado/$', 'administracion.views.eliminar_fase'),

################################################URL ROL#################################################################
    url(r'^administracion/roles/$', 'administracion.views.administrar_roles'),
    url(r'^administracion/roles/nuevo/$', 'administracion.views.crear_rol'),
    url(r'^administracion/roles/asignar/$', 'administracion.views.vista_asignar_rol'),
    url(r'^administracion/roles/asignar/(?P<id_usuario_p>\d+)$', 'administracion.views.asignar_rol'),
    url(r'^administracion/roles/detalle/(?P<idRol>\d+)$', 'administracion.views.detalle_rol'),
    url(r'^administracion/roles/(?P<idRol>\d+)/modificar/$', 'administracion.views.modificar_rol'),
    url(r'^administracion/roles/(?P<idRol>\d+)/eliminar/$', 'administracion.views.vista_eliminar_rol'),
    url(r'^administracion/roles/(?P<idRol>\d+)/eliminado/$', 'administracion.views.eliminar_rol'),

###############################################URL CREDENCIAL###########################################################
    url(r'^administracion/credenciales/$', 'administracion.views.administrar_credencial'),
)
