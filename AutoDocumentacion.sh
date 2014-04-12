#!/bin/bash

#Limpiar la carpeta docp
rm -rf docp/*

#Creacion de los archivos base para la documentacion
echo Seguir la guia Sphinx.txt para completar este paso
cd docp
sphinx-quickstart

cd ..

#Cracion de .rst de todos los modulos del proyecto
sphinx-apidoc -f -o docp/ .

#Configuracion del archivo conf.py
cd docp

match='import os'
insert1="os.environ['DJANGO_SETTINGS_MODULE'] = 'SGP.settings'"
insert2="sys.path.insert(0, os.path.abspath('..'))"
insert3="language = 'spanish'"
file='conf.py'

sed -i "s/$match/$match\n$insert1/" $file
sed -i "s/$match/$match\n$insert2/" $file
sed -i "s/$match/$match\n$insert3/" $file


#Creaicion de los archivos html
make html

