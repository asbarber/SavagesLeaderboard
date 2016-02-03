#!/bin/bash

# navigate
cd ..

# packages
pip install -r admin/admin-reqs.txt

# setup database
python manage.py makemigrations
python manage.py migrate 
python manage.py loaddata users.json
python manage.py loaddata achievements.json
# python manage.py createsuperuser