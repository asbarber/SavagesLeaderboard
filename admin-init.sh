#!/bin/bash

# packages
pip install -r admin-reqs.txt

# setup database
cd mysite
python manage.py makemigrations
python manage.py migrate 
python manage.py loaddata users.json
python manage.py loaddata achievements.json
# python manage.py createsuperuser
cd ..