import os
import sys
sys.path = ['/home/alx/SGP'] + sys.path
os.environ['DJANGO_SETTINGS_MODULE'] = 'SGP.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
