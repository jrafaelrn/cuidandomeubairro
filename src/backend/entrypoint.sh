#!/bin/bash

set -e

echo "Waiting for postgres... 10 seconds"
sleep 10

# Create database schema
PGPASSWORD=$POSTGRES_PASSWORD psql -h $POSTGRES_HOST -U $POSTGRES_USER -d $POSTGRES_DB -f tools/cmb.sql

python3 classes/api/api_despesa.py & python3 run_etl_cmb.py && fg