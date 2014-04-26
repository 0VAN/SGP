__author__ = 'jf'
# -*- encoding: utf-8 -*-

from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User, Group
from administracion.models import Proyecto, Fase, Atributo
from desarrollo.models import Item

class ItemForm(forms.ModelForm):
    """
    Formulario para la creacion de items
    Hereda de forms.ModelForm y utiliza la clase Group para
    agregar ciertos campos a la hora de la creacion/modificacion/eliminacion
    """

    class Meta:
        model = Item
        exclude = ['Usuario', 'Fase', 'Fecha', 'Estado', 'Version']