#!/bin/bash

# Borrar los archivos anteriores
echo -e "\nBorrando archivos antiguos"
sudo rm -r /var/www/SGP/
echo -e "\nArchivos borrados"

cd /var/www/

echo -e "\nClonamos el repositorio en /var/www/"
git clone git://github.com/0van/SGP.git
echo -e "\nRepositorio clonado"
# Copiar los archivos al directorio servido por apache2

echo -e "\nLe otorgamos los permisos al directorio"
chmod -R 777 /var/www/SGP/

echo -e "----Configurando Apache----"
mv /var/www/SGP/conf/*.conf /etc/apache2/sites-available/
mv /var/www/SGP/conf/*.wsgi /var/www/
rm -r /var/www/SGP/conf
cp -r /usr/local/lib/python2.7/dist-packages/django/contrib/admin/static/ /var/www/SGP/

echo -e "\nHacemos checkout del Tag"
git checkout 1.4
echo -e "\nActivando los sitios [SGP] en Apache"
a2ensite SGP.conf

echo -e "\nRecargando Apache"
service apache2 reload

# TODO: Verificar si estos datos en /etc/hosts antes de agregarlos, actualmente se agregan cada vez que se ejecuta el archivo
# TODO: Eliminar al desinstalar la aplicacion
echo -e "----Fix[sin DNS]: Agrega el nombre y direccion de la pagina a los hosts conocidos de la maquina.----"
echo "127.0.0.1 sgp.com" >> /etc/hosts
echo "127.0.0.1 sgp.com/static/" >> /etc/hosts

echo "----Fin----"

firefox sgp.com/