#!/bin/bash

. bin/activate
python manage.py sync_all -f
chown leonardo:leonardo src/static/* -R
sh server_run.sh
