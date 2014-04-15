__author__ = 'sgp'

from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from administracion.models import Proyecto

class UsuarioForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'telefono', 'direccion', 'observacion')

class ProyectoForm(ModelForm):
    class Meta:
        model = Proyecto
