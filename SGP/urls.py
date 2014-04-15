from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'SGP.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'administracion.views.lista_usuarios'),
    url(r'^$', 'administracion.views.iniciar_sesion'),
    url(r'^ingresar/$', 'administracion.views.iniciar_sesion'),
    url(r'^privado/$','administracion.views.privado'),
    url(r'^cerrar/$', 'administracion.views.cerrar_sesion'),
    url(r'^administracion/$', 'administracion.views.administracion'),
    url(r'^nuevoUsuario/$', 'administracion.views.nuevo_usuario'),
    url(r'^nuevoProyecto/$', 'administracion.views.nuevo_proyecto'),
    url(r'^listaProyecto/$', 'administracion.views.lista_proyectos'),
    url(r'^modificarUsuario/(?P<id_usuario>\d+)/$', 'administracion.views.actualiza_usuario'),
)
