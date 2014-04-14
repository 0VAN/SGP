
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

User.add_to_class('direccion', models.FloatField(null=True, blank=True))
User.add_to_class('telefono', models.PositiveIntegerField(null=True, blank=True))
User.add_to_class('observacion', models.PositiveIntegerField(null=True, blank=True))


