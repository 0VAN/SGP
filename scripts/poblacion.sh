#!/bin/bash
echo 5- Se puebla la base de datos con 1 usuario lider y 4 desarrolladores
cd ..
python manage.py loaddata scripts/poblacion.json