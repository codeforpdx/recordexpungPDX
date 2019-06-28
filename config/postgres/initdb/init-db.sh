#!/bin/bash
set -e

# Create database and docker user.
psql \
    -v ON_ERROR_STOP=1 \
    -v POSTGRES_USER="${POSTGRES_USERNAME}" \
    -v POSTGRES_PASSWORD="${POSTGRES_PASSWORD}" \
    <<-EOSQL
    CREATE USER docker;
    CREATE DATABASE record_expunge;
    ALTER USER docker WITH SUPERUSER CREATEDB CREATEROLE REPLICATION BYPASSRLS;
EOSQL

# Create tables and functions.

psql \
    -v ON_ERROR_STOP=1 \
    -v POSTGRES_USER="${POSTGRES_USERNAME}" \
    -v POSTGRES_PASSWORD="${POSTGRES_PASSWORD}" \
    --username "${POSTGRES_USERNAME}" \
    -f /docker-entrypoint-initdb.d/scripts/create-tables-and-functions.sql
