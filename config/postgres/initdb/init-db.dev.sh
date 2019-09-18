#!/bin/bash
set -e

# Create database

psql \
    -v ON_ERROR_STOP=1 \
    -U "${POSTGRES_USERNAME}" \
    -d "${POSTGRES_USERNAME}" \
    -v POSTGRES_PASSWORD="${POSTGRES_PASSWORD}" \
    <<-EOSQL
    CREATE DATABASE ${PGDATABASE};
EOSQL

# Create tables and functions.

 # this syntax stopped working I guess? -v POSTGRES_USER="${POSTGRES_USERNAME}"
 # replaced with: -U "${POSTGRES_USERNAME}"

psql \
    -v ON_ERROR_STOP=1 \
    -U "${POSTGRES_USERNAME}" \
    -v POSTGRES_PASSWORD="${POSTGRES_PASSWORD}" \
    -d "${PGDATABASE}" \
    -f /docker-entrypoint-initdb.d/scripts/create-tables.sql

psql \
    -v ON_ERROR_STOP=1 \
    -U "${POSTGRES_USERNAME}" \
    -v POSTGRES_PASSWORD="${POSTGRES_PASSWORD}" \
    -d "${PGDATABASE}" \
    -f /docker-entrypoint-initdb.d/scripts/create-functions.sql

psql \
    -v ON_ERROR_STOP=1 \
    -U "${POSTGRES_USERNAME}" \
    -v POSTGRES_PASSWORD="${POSTGRES_PASSWORD}" \
    -d "${PGDATABASE}" \
    -f /docker-entrypoint-initdb.d/scripts/initial_credentials.dev.sql
