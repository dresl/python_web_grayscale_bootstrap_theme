#!/bin/bash

. bin/activate
python manage.py sync_all -f --nocompress
sh server_run.sh
