#!/bin/bash
set -ex

CWD=`dirname $0`
ENV=${CWD}/../${1:-client.env}

source ${ENV}

createdb ${PGDATABASE}
psql -v ON_ERROR_STOP=1 -d ${PGDATABASE} -f ${CWD}/scripts/create-tables.sql
psql -v ON_ERROR_STOP=1 -d ${PGDATABASE} -f ${CWD}/scripts/create-functions.sql
psql -v ON_ERROR_STOP=1 -d ${PGDATABASE} -f ${CWD}/scripts/initial_credentials.dev.sql
