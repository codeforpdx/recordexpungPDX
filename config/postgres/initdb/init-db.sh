#!/bin/bash
set -e

# Create database and docker user.
psql \
    -v ON_ERROR_STOP=1 \
    -v POSTGRES_USER="${PGUSER}" \
    -v POSTGRES_PASSWORD="${PGPASSWORD}" \
    <<-EOSQL
    CREATE USER docker;
    CREATE DATABASE record_expunge;
    ALTER USER docker WITH SUPERUSER CREATEDB CREATEROLE REPLICATION BYPASSRLS;
EOSQL

# Create tables and functions.

psql \
    -v ON_ERROR_STOP=1 \
    -v POSTGRES_USER="${PGUSER}" \
    -v POSTGRES_PASSWORD="${PGPASSWORD}" \
    --username "${PGUSER}" \
    -f /docker-entrypoint-initdb.d/scripts/create-tables-and-functions.sql
