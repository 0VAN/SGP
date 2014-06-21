#!/bin/bash

echo "Tags SGP"
PS3='Seleccione el tag a descargar: '
options=("1.0" "1.1" "1.2" "1.3" "1.4" "1.5" "Salir")
select opt in "${options[@]}"
do
    case $opt in
        "${options[0]}")
            tag="1.0"
            break
            ;;
        "${options[1]}")
            tag="1.1"
            break
            ;;
        "${options[2]}")
            tag="1.2"
            break
            ;;
        "${options[3]}")
            tag="1.3"
            break
            ;;
        "${options[4]}")
            tag="1.4"
            break
            ;;
        "${options[5]}")
            tag="1.5"
            break
            ;;
        "${options[6]}")
            exit
            ;;
        *) echo Opcion no valida;;
    esac
done

# Borrar los archivos anteriores
echo -e "\nBorrando archivos antiguos"
sudo rm -r /var/www/SGP/
echo -e "\nArchivos borrados"

cd /var/www/

echo -e "\nClonamos el repositorio en /var/www/"
sudo git clone git://github.com/0van/SGP.git
echo -e "\nRepositorio clonado"
# Copiar los archivos al directorio servido por apache2

echo -e "\nLe otorgamos los permisos al directorio"
sudo chmod -R 777 /var/www/SGP/

echo -e "----Configurando Apache----"
sudo mv /var/www/SGP/conf/*.conf /etc/apache2/sites-available/
sudo mv /var/www/SGP/conf/*.wsgi /var/www/
sudo rm -r /var/www/SGP/conf
sudo cp -r /usr/local/lib/python2.7/dist-packages/django/contrib/admin/static/ /var/www/SGP/
echo -e "\nHacemos checkout del Tag"
cd /var/www/SGP/
sudo git checkout -f $tag
sudo chmod -R 777 /var/www/SGP/

echo -e "\nCargamos los datos iniciales"
case $opt in
    "${options[0]}")
        sudo sed -i '65s/sgparj/postgres/g' /var/www/SGP/SGP/settings.py
        sudo sed -i '64s/sgp/postgres/g' /var/www/SGP/SGP/settings.py
        python manage.py syncdb
        python manage.py loaddata fixtures/Usuarios.json
        ;;
    "${options[1]}")
        sudo ./Creacion\ de\ Base\ de\ Datos.sh
        ;;
    "${options[2]}")
        sudo ./Creacion\ de\ Base\ de\ Datos.sh
        ;;
    "${options[3]}")
        sudo ./Creacion\ de\ Base\ de\ Datos.sh
        sudo ./poblacion.sh
        ;;
    "${options[4]}")
        cd scripts/
        sudo ./baseDeDatos.sh
        sudo ./poblacion.sh
        ;;
    "${options[5]}")
        cd scripts/
        sudo ./baseDeDatos.sh
        sudo ./poblacion.sh
        ;;
esac

echo -e "\nActivando los sitios [SGP] en Apache"
sudo a2ensite SGP.conf

echo -e "\nRecargando Apache"
sudo service apache2 reload

# TODO: Verificar si estos datos en /etc/hosts antes de agregarlos, actualmente se agregan cada vez que se ejecuta el archivo
# TODO: Eliminar al desinstalar la aplicacion
echo -e "----Fix[sin DNS]: Agrega el nombre y direccion de la pagina a los hosts conocidos de la maquina.----"
sudo echo "127.0.0.1 sgp.com" >> /etc/hosts
sudo echo "127.0.0.1 sgp.com/static/" >> /etc/hosts

echo "----Fin----"



firefox "sgp.com" &
