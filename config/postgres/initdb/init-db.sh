#!/bin/bash
set -e

# Create database and docker user.
psql \
    -v ON_ERROR_STOP=1 \
    -v POSTGRES_USER="${POSTGRES_USER}" \
    -v POSTGRES_PASSWORD="${POSTGRES_PASSWORD}" \
    <<-EOSQL
    CREATE USER docker;
    CREATE DATABASE record_expunge;
    ALTER USER docker WITH SUPERUSER CREATEDB CREATEROLE REPLICATION BYPASSRLS;
EOSQL

# Create tables.
psql \
    -v ON_ERROR_STOP=1 \
    -v POSTGRES_USER="${POSTGRES_USER}" \
    -v POSTGRES_PASSWORD="${POSTGRES_PASSWORD}" \
    --username "${POSTGRES_USER}" \
    -f /docker-entrypoint-initdb.d/scripts/create-tables.sql