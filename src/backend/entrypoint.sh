#!/bin/bash

set -e

echo "Waiting for postgres... 10 seconds"
sleep 10

pwd
ls -lah

psql -U $POSTGRES_USER -d $POSTGRES_DB -f cmb.sql

python run_etl_cmb.py


