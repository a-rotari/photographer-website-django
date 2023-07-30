#!/bin/sh

python manage.py makemigrations --no-input
python manage.py migrate --no-input
python manage.py collectstatic --no-input
#sh -c 'python manage.py createsuperuser --noinput \
#    --username=admin \
#    --email=admin@example.com'

gunicorn marie_site.wsgi:application --bind 0.0.0.0:8000
