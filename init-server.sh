#!/bin/bash

# cd /var/www/html
# python manage.py runserver 0.0.0.0:8000


# run server (on server machine)
sudo stop apache2
sudo python manage.py runserver 0.0.0.0:80
