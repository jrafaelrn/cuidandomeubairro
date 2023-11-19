#!/bin/bash

set -e

# Create database schema
PGPASSWORD=$POSTGRES_PASSWORD psql -h $POSTGRES_HOST -U $POSTGRES_USER -d $POSTGRES_DB -f tools/cmb.sql


# Inicia 2 processos em paralelo
# 1. API Despesa - Usada pelo frontend para consultar os dados
# 2. ETL - Processo que faz a carga dos dados no banco de dados
python3 classes/api/api_despesa.py & python3 run_etl_cmb.py && fg