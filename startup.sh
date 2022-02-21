#!/bin/sh

gunicorn backend.wsgi:application --bind 0.0.0.0:80
&& celery -A backend worker --loglevel=info
&& celery -A backend beat --loglevel=info