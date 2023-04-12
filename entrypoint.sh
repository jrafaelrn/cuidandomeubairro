#!/bin/bash

set -e

pwd
ls -lah

cd ./import_layouts/states/sp/sao_paulo/gastos_abertos

echo "Waiting for postgres... 5 seconds"
sleep 5


# Check if PostGIS extension is already installed
psql_output=$(PGPASSWORD=$POSTGRES_PASSWORD psql -h $POSTGRES_HOST -p $POSTGRES_PORT -U $POSTGRES_USER -d $POSTGRES_DB -tAc 'SELECT extname FROM pg_extension')

if echo $psql_output | grep -q postgis; then
    echo "----> PostGIS extension already exists!"
else
   PGPASSWORD=$POSTGRES_PASSWORD psql -h $POSTGRES_HOST -p $POSTGRES_PORT -U $POSTGRES_USER -d $POSTGRES_DB -c 'CREATE EXTENSION postgis;'
fi


python setup.py install
#python3 cuidando_utils/setup.py install

#export FLASK_APP=app.py
#python manage.py run


flask initdb
flask run


