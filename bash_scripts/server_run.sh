#!bin/bash

ip=$(ifconfig eth1 | grep 'inet addr:' | cut -d: -f2 | awk '{ print $1}')

if python manage.py runserver $ip:80 ; then
    echo "Command succeeded"
else
    echo "Command failed, preparing comand fuser -k 80/tcp"
    fuser -k 80/tcp
    python manage.py runserver $ip:80
fi
