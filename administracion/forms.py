__author__ = 'sgp'

from django.forms import ModelForm
from django import forms
from administracion.models import Fase

class FaseForm(ModelForm):
    class Meta:
        model = Fase
        exclude = ['Usuario']