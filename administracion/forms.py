# -*- encoding: utf-8 -*-
from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm, ReadOnlyPasswordHashField, UserChangeForm
from django.contrib.auth.models import User, Group
from administracion.models import Proyecto, Fase, Atributo, TipoDeItem
from django.contrib.auth.forms import UserCreationForm, ReadOnlyPasswordHashField
from django.contrib.auth.models import User, Group, Permission
from administracion.models import Proyecto, Fase
from django.contrib.admin.widgets import FilteredSelectMultiple
from functools import partial

DateInput = partial(forms.DateInput, {'class': 'datepicker'})

from desarrollo.forms import MyForm

class AsignarRol(MyForm):
    """
    Formulario para la asignacion de roles a los usuarios
    Hereda del forms.ModelForm y utiliza la clase user
    para agregar ciertos campos de la clase a la hora de la asignacion
    """
    class Meta:
        model = User
        fields = ['groups']
        labels = {
            'groups': ('Roles'),
        }
        help_texts = {
            'groups': ('Selecciones el/los roles deseados que desea asignar al usuario.'),
        }


class ProyectoForm(ModelForm):
    """
    Formulario para la creacion de proyectos en el sistema
    Hereda de ModelForm y utiliza la clase Proyecto
    para agregar ciertos campos de la clase a la hora de la creacion
    """
    Fecha_inicio = forms.DateField(widget=DateInput())
    Fecha_finalizacion = forms.DateField(widget=DateInput())
    class Meta:
        model = Proyecto
        exclude = ['Usuario', 'Estado', 'Usuarios']



class UsuarioModForm(forms.ModelForm):
    """
    Formluario para la modificacion de usuarios
    Hereda de forms.ModelForm y utiliza la clase user para
    agregar ciertos campos a la hora de la modificacion
    """
    error_css_class = 'list-group-item-danger'

    class Meta:
        model = User
        exclude = '__all__'

    def __init__(self, *args, **kwargs):
            super(UsuarioModForm, self).__init__(*args, **kwargs)
            for field_name, field in self.fields.items():
                field.widget.attrs['class'] = 'form-control'
            f = self.fields.get('user_permissions', None)
            if f is not None:
                f.queryset = f.queryset.select_related('content_type')

    def clean_password(self):
            # Regardless of what the user provides, return the initial value.
            # This is done here, rather than on the field, because the
            # field does not have access to the initial value
            return self.initial["password"]



class UsuarioDelForm(MyForm):
    """
    Formulario para el la eliminacion logica del usuario
    Hereda de forms.ModelForm y utiliza la clase user para
    agregar ciertos campos a la hora de la eliminacion
    """
    class Meta:
        model = User
        fields = ('is_active',)

class FaseForm(MyForm):
    """
    Formulario para el la creacion de fases
    Hereda de forms.ModelForm y utiliza la clase Fase para
    agregar ciertos campos a la hora de la creacion/modificacion
    """
    class Meta:
        model = Fase
        exclude = ['Usuario', 'Proyecto']

class RolForm(MyForm):
    permissions = forms.ModelMultipleChoiceField(queryset=Permission.objects.all(),label=('Seleccionar permisos'),
                                          widget=FilteredSelectMultiple(('Permisos'),False,))

    """
    Formulario para la creacion de roles
    Hereda de forms.ModelForm y utiliza la clase Group para
    agregar ciertos campos a la hora de la creacion/modificacion/eliminacion
    """
    class Meta:
        model = Group
        exclude = ['Usuario']
    class Media:
        css = {'all':('/static/css/filteredselectwidget.css',),}
        # jsi18n is required by the widget
        js = ('/admin/jsi18n/',)

class AtributoForm(MyForm):
    """
    Formulario para el la creacion de atributos
    Hereda de forms.ModelForm y utiliza la clase Group para
    agregar ciertos campos a la hora de la creacion/modificacion/eliminacion
    """
    class Meta:
        model = Atributo
        exclude = ['Usuario', 'Fase']



class tipoItemForm(MyForm):
    """

    """
    class Meta:
        model = TipoDeItem
        exclude = ['Usuario', 'Fase']
