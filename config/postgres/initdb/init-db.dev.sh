#!/bin/bash
set -e

# Create database and docker user.
echo "POSTGRES_USERNAME=${POSTGRES_USERNAME}"
echo "POSTGRES_PASSWORD=${POSTGRES_USERNAME}"
psql \
    -v ON_ERROR_STOP=1 \
    -U "${POSTGRES_USERNAME}" \
    -v POSTGRES_PASSWORD="${POSTGRES_PASSWORD}" \
    <<-EOSQL
    CREATE DATABASE ${DB_NAME};
EOSQL

# Create tables and functions.

 # this stopped working? -v POSTGRES_USER="${POSTGRES_USERNAME}" \

psql \
    -v ON_ERROR_STOP=1 \
    -U "${POSTGRES_USERNAME}" \
    -v POSTGRES_PASSWORD="${POSTGRES_PASSWORD}" \
    -d "${DB_NAME}" \
    -f /docker-entrypoint-initdb.d/scripts/create-tables-and-functions.sql


psql \
    -v ON_ERROR_STOP=1 \
    -U "${POSTGRES_USERNAME}" \
    -v POSTGRES_PASSWORD="${POSTGRES_PASSWORD}" \
    -d "${DB_NAME}" \
    -f /docker-entrypoint-initdb.d/scripts/initial_credentials.sql
