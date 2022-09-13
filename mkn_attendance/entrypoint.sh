#!/bin/sh


python manage.py migrate --noinput
python manage.py collectstatic --noinput


gunicorn mkn_attendance.wsgi:application --bin 0.0.0.0:8000
