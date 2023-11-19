#!/bin/bash

set -e

# Check if DB is online
if netstat -tuplen | grep 5499 | grep LISTEN; then
    echo "localhost:5499 - Database is online"
    echo "Waiting for postgres... 10 seconds"
    sleep 10
else
    echo "localhost:5499 - Database is offline..."
    echo "Waiting for postgres... 600 seconds"
    sleep 600
fi

# Create database schema
PGPASSWORD=$POSTGRES_PASSWORD psql -h $POSTGRES_HOST -U $POSTGRES_USER -d $POSTGRES_DB -f tools/cmb.sql



# Check if Nominatim API is online
if netstat -tuplen | grep 8088 | grep LISTEN; then
    echo "localhost:8088 - Nominatim is online"
    echo "Waiting 3 seconds"
    sleep 3
else
    echo "localhost:8088 - Nominatim is offline..."
    echo "Waiting for Nominatim... 1 hour"
    sleep 3600
fi



python3 classes/api/api_despesa.py & python3 run_etl_cmb.py && fg