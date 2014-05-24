__author__ = 'alx'
# -*- encoding: utf-8 -*-

from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import User

class UsuarioGestionForm(forms.ModelForm):
    """
    Formluario para la modificacion de usuarios
    Hereda de forms.ModelForm y utiliza la clase user para
    agregar ciertos campos a la hora de la modificacion
    """
    username = forms.RegexField(
        label=("Nombre de usuario"), max_length=30, regex=r"^[\w.@+-]+$",
        help_text=("Required. 30 characters or fewer. Letters, digits and "
                      "@/./+/-/_ only."),
        error_messages={
            'invalid': ("This value may contain only letters, numbers and "
                         "@/./+/-/_ characters.")})
    password = ReadOnlyPasswordHashField(label=("Contraseña"),
        help_text=("Las contraseñas no se almacenan en bruto, así que no hay manera de ver la contraseña del usuario,"
                   " pero se puede cambiar mediante <a href=\"password/\">este formulario</a>. "))
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name', 'telefono', 'direccion')
        fieldsets = [
        ( None,               {'fields': ['username', 'password']}),
        ('Informacion personal', {'fields': ['email', 'first_name', 'last_name', 'telefono', 'direccion'], 'classes': ['collapse']}),
        ]

    def __init__(self, *args, **kwargs):
            super(UsuarioGestionForm, self).__init__(*args, **kwargs)
            f = self.fields.get('user_permissions', None)
            if f is not None:
                f.queryset = f.queryset.select_related('content_type')

    def clean_password(self):
            # Regardless of what the user provides, return the initial value.
            # This is done here, rather than on the field, because the
            # field does not have access to the initial value
            return self.initial["password"]

    widgets = {}