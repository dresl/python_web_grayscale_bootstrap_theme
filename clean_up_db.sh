#!bin/bash
su -c "psql -c \"drop database grayscale_db\"" postgres
su -c "psql -c \"create database grayscale_db\"" postgres
su -c "psql -c \"GRANT ALL PRIVILEGES ON DATABASE grayscale_db to grayscale\"" postgres

sh remove_migrations.sh
python manage.py makemigrations
python manage.py migrate
sh create_data_db.sh
sh server_run.sh
