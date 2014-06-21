#!/bin/bash


cd ../

# Borrar los archivos anteriores
echo -e "\nBorrando archivos antiguos"
rm -r /var/www/SGP/
echo -e "Archivos borrados\n"

# TODO: Eliminar al desinstalar la aplicacion
# Copiar los archivos al directorio servido por apache2
echo "Copiando archivos"
cd ..
cp -r ./SGP/ /var/www/SGP/
chmod -R 777 /var/www/SGP/
echo -e "Archivos copiados\n"

# TODO: Eliminar al desinstalar la aplicacion
echo -e "----Configurando Apache----"
mv /var/www/SGP/conf/*.conf /etc/apache2/sites-available/
mv /var/www/SGP/conf/*.wsgi /var/www/
rm -r /var/www/SGP/conf
cp -r /usr/local/lib/python2.7/dist-packages/django/contrib/admin/static/ /var/www/SGP/
echo -e "Activando los sitios [SGP] en Apache"
a2ensite SGP.conf

echo -e "Correr Apache"
/etc/init.d/apache2 restart

echo -e "Recargando Apache"
service apache2 reload

# TODO: Verificar si estos datos en /etc/hosts antes de agregarlos, actualmente se agregan cada vez que se ejecuta el archivo
# TODO: Eliminar al desinstalar la aplicacion
echo -e "----Fix[sin DNS]: Agrega el nombre y direccion de la pagina a los hosts conocidos de la maquina.----"
echo "127.0.0.1 sgp.com" >> /etc/hosts
echo "127.0.0.1 sgp.com/static/" >> /etc/hosts

echo "----Fin----"

firefox sgp.com/