#!/bin/bash

. ../bin/activate
python manage.py sync_all -f --nocompress
