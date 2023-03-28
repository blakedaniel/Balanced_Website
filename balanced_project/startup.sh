#!/bin/bash

# migrate all models
python manage.py makemigrations --scriptable
python manage.py migrate

#migrate betteretf models
python manage.py makemigrations betteretf --scriptable
python manage.py migrate betteretf

# start django development server on port 8000
python manage.py runserver 0.0.0.0:8000