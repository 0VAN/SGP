#!/bin/bash
echo "Tags SGP"
PS3='Seleccione el tag a descargar: '
options=("1.0" "1.1" "1.2" "1.3" "1.4" "Salir")
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
echo $tag