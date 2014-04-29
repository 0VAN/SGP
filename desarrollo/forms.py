__author__ = 'jf'
# -*- encoding: utf-8 -*-

from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User, Group
from administracion.models import Proyecto, Fase, Atributo, TipoDeItem
from desarrollo.models import Item

class MyForm(forms.ModelForm):

    error_css_class = 'list-group-item-danger'
    def __init__(self, *args, **kwargs):
        super(MyForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ItemForm(MyForm):
    """
    Formulario para la creacion de items
    Hereda de forms.ModelForm y utiliza la clase Group para
    agregar ciertos campos a la hora de la creacion/modificacion/eliminacion
    """

    class Meta:
        model = Item
        exclude = ['Usuario', 'Fase', 'Fecha', 'Estado', 'Version']

