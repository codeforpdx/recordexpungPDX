#!/bin/bash
set -e

cwd=`dirname $0`

createdb ${PGDATABASE}
psql -f ${cwd}/scripts/create-tables.sql
psql -f ${cwd}/scripts/create-functions.sql
psql -f ${cwd}/scripts/initial_credentials.dev.sql
