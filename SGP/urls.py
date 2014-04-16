from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'SGP.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admUsuario', include('django.contrib.auth.urls')),
    url(r'^admUsuario/modificar/password/$', 'django.contrib.auth.views.password_change',
        {'current_app': 'administracion',
         'template_name': 'usuario/modificar_passwdform.html',
         'post_change_redirect': 'admUsuario/modificar/password/done'},
        name='password',),


    url(r'^admUsuario/modificar/password/done$', 'django.contrib.auth.views.password_change_done',
        {'template_name': 'usuario/modificar_passwdform.html'}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'administracion.views.iniciar_sesion'),
    url(r'^ingresar/$', 'administracion.views.iniciar_sesion'),
    url(r'^privado/$','administracion.views.privado'),
    url(r'^cerrar/$', 'administracion.views.cerrar_sesion'),
    url(r'^administracion/$', 'administracion.views.administracion'),

    url(r'^admUsuario/$', 'administracion.views.administrar_usuario'),
    url(r'^admUsuario/nuevo/$', 'administracion.views.crear_usuario'),
    url(r'^admUsuario/modificar/$', 'administracion.views.modificar_usuario1'),
    url(r'^admUsuario/modificar/(?P<id_usuario>\d+)$$', 'administracion.views.modificar_usuario2'),

    url(r'^usuario/detalle/(?P<id_usuario>\d+)$$', 'administracion.views.detalle_usuario'),


    url(r'^nuevoProyecto/$', 'administracion.views.nuevo_proyecto'),
    url(r'^listaProyecto/$', 'administracion.views.lista_proyectos'),

)
