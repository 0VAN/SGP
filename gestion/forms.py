__author__ = 'killua'

from gestion.models import *
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple

class ComiteForm(forms.ModelForm):
    class Meta:
        model = ComiteDeCambio
        exclude = ['Usuario1','Proyecto']

class LineBaseForm(forms.ModelForm):
    Items = forms.ModelMultipleChoiceField(queryset=Item.objects.all(),label=('Seleccionar Items'),
                                          widget=FilteredSelectMultiple(('Items'),False,))
    class Meta:
        model = LineBase
        exclude = ['Usuario','Fecha','Fase']

    class Media:
        css = {'all':('/static/css/filteredselectwidget.css',),}
        # jsi18n is required by the widget
        js = ('/static/js/jsi18n.js',)