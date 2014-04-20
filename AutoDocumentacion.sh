#!/bin/bash

#Cracion de .rst de todos los modulos del proyecto
sphinx-apidoc -f -o doc/ .
cd doc/
#Creaicion de los archivos html
make html

