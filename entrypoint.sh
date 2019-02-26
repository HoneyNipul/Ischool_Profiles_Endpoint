#!/bin/bash

echo "Running Migrations"
python /var/webapp/manage.py migrate

echo "Collecting Static Assets"
python /var/webapp/manage.py collectstatic --noinput

/usr/local/bin/uwsgi --ini /etc/uwsgi/uwsgi.ini