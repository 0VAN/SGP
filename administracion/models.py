
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Fase(models.Model):
    Nombre = models.CharField(max_length=50)
    Descripcion = models.TextField()
    Usuario = models.ForeignKey(User)
    Fecha = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.Nombre


