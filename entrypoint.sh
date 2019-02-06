#!/bin/sh

python manage.py migrate
gunicorn --bind 0.0.0.0:80 ISA.wsgi:application
