#!/bin/bash



cat administracion/models_roles.py >administracion/models.py

python manage.py syncdb