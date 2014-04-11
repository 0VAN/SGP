from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'SGP.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    #url(r'^$', 'administracion.views.lista_usuarios'),
    url(r'^$', 'administracion.views.nuevo_usuario'),
    url(r'^ingresar/$', 'administracion.views.ingresar'),
    url(r'^privado/$','administracion.views.privado'),
    url(r'^cerrar/$', 'administracion.views.cerrar'),
    url(r'^administracion/$', 'administracion.views.administracion'),

)
