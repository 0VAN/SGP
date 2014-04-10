__author__ = 'sgp'

from django.forms import ModelForm
from django import forms
from administracion.models import Usuario

class UsuarioForm(ModelForm):
    class Meta:
        model = Usuario
