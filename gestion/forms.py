__author__ = 'killua'

from gestion.models import *
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from desarrollo.forms import MyForm

class ComiteForm(forms.ModelForm):
    class Meta:
        model = ComiteDeCambio
        exclude = ['Usuario1', 'Proyecto']
        fields = ['Usuario2', 'Usuario3']
        labels = {
            'Usuario2': ('Integrante 2'),
            'Usuario3': ('Integrante 3'),
        }

class LineBaseForm(MyForm):
    Items = forms.ModelMultipleChoiceField(queryset=Item.objects.all(),label=('Seleccionar Items'),
                                          widget=FilteredSelectMultiple(('Items'),False,))
    class Meta:
        model = LineBase
        exclude = ['Usuario','Fecha','Fase']

    class Media:
        css = {'all':('/static/css/filteredselectwidget.css',),}
        # jsi18n is required by the widget
        js = ('/static/js/jsi18n.js',)


class SolicitudCambioForm(MyForm):
    items = forms.ModelMultipleChoiceField(queryset=Item.objects.all(),label=('Seleccionar Items'),
                                          widget=FilteredSelectMultiple(('Items'),False,))
    class Meta:
        model = SolicitudCambio
        exclude = ['fase', 'proyecto', 'usuario', 'fecha', 'estado']

    class Media:
        css = {'all':('/static/css/filteredselectwidget.css',),}
        # jsi18n is required by the widget
        js = ('/static/js/jsi18n.js',)