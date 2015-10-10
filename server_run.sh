#!bin/bash
if python manage.py runserver 192.168.0.103:80 ; then
    echo "Command succeeded"
else
    echo "Command failed, preparing comand fuser -k 80/tcp"
    fuser -k 80/tcp
    python manage.py runserver 192.168.0.103:80
fi
