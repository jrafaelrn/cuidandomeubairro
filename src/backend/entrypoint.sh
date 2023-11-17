#!/bin/bash

set -e

# Check if localhost:5000 is online
if nc -z localhost 5000; then
    echo "localhost:5000 is online"
    echo "Waiting for postgres... 10 seconds"
    sleep 10
else
    echo "localhost:5000 is not online..."
    echo "Waiting for postgres... 10000 seconds"
    sleep 10000
fi

# Create database schema
PGPASSWORD=$POSTGRES_PASSWORD psql -h $POSTGRES_HOST -U $POSTGRES_USER -d $POSTGRES_DB -f tools/cmb.sql

python3 classes/api/api_despesa.py & python3 run_etl_cmb.py && fg