SGP
===

Proyecto de Ing. de software 2
HERRAMIENTAS A UTILIZAR
*RECOMENDACIONES: - HACER SUDO SU Y LOGEARSE COMO ROOT PARA NO INGRESAR LAS CONTRASENHA CADA MOMENTO
				  - LUEGO DE EJECUTAR CADA COMANDO EJECUTAR sudo apt-get update PARA QUE TODO FUNCIONE BIEN
				  - AUNQUE PIENSES QUE TENGAS TODO EJECUTA TODOS(MENOS LO DE PYCHARM) LOS COMANDOS DE VUELTA POR LAS DUDAS TOTAL SI YA LOS TENES NO SE TE VA INSTALAR NADA

INSTALAR EN ESTE ORDEN

1- POSTGRESQL(BASE DE DATOS)

sudo apt-get install postgresql 

2- INSTALAR PSYCOPG2(EXTENSION QUE SIRVE PARA USAR SQL CON CODIGO PYTHON)

sudo apt-get install libpq-dev

sudo apt-get install python-psycopg2

3- INSTALAR DJANGO(FRAMEWORK A UTILIZAR)

sudo apt-get install python-pip

sudo pip install Django

4- INSTALAR JAVA(NECESARIO PARA PYCHARM)

sudo add-apt-repository ppa:webupd8team/java

sudo apt-get install oracle-java7-installer

sudo apt-get install oracle-java7-set-default

5- INSTALAR GIT(CONTROLADOR DE VERSIONES)

sudo apt-get install git

6- INSTALAR PYCHARM(IDE A UTILIZAR)

Descargar Pycharm de la pag oficial, ir al donde se encuentra el .tar.gz y ejecutar el siguiente comando

sudo mkdir -p /opt/PyCharm

sudo tar -zxvf pycharm-professional-3.1.1.tar.gz --strip-components 1 -C /opt/PyCharm

sudo /opt/PyCharm/bin/pycharm.sh

7- SPHINX(GENERADOR DE DOCUMENTACION)

sudo easy_install -U Sphinx

reversiones
pip install django-reversion

Pagina oficial de las reversiones
http://github.com/etianen/django-reversion



pydot- para los grafos

sudo apt-get install graphviz libgraphviz-dev pkg-config

sudo easy_install pyparsing

descargar pydot-1.0.28.tar.gz del enlace  https://pypi.python.org/pypi/pydot

descomprimir e ir a la carpeta pydot-1.0.28 y ejecutar

sudo python setup.py install




Para facilitar las cosas con la base de datos puedes hacer que tu usaurio sea un superUsuario de la BD

Iniciar sesion como usuario postgres
$ sudo -u postgres psql postgres

El pass de postgres = postgres
# \password postgres

crear el usuario
CREATE USER miUsuario PASSWORD 'miPassword';

darle permisos de super usuario
ALTER ROLE miUsuario WITH SUPERUSER;









