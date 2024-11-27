#!/bin/sh

# Выполнение миграций и других необходимых команд
python manage.py migrate --run-syncdb
gunicorn ERP.wsgi:application --bind 0.0.0.0:8080 --reload -w 4
