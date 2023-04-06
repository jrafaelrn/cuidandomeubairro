#!/bin/bash

set -e

pwd
ls -lah

cd gastos_abertos

pwd
ls -lah

python3 setup.py install
#python3 cuidando_utils/setup.py install

#export FLASK_APP=app.py
#flask run


fab reset initdb importdata generate_jsons
python manage.py run

