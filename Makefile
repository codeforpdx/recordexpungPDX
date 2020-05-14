.PHONY: clean

REQUIREMENTS_TXT := src/backend/requirements.txt
OSFLAG 	:=
ifeq ($(OS),Windows_NT)
	OSFLAG = WIN32
endif

clean:
ifeq ($(OSFLAG), WIN32)
	del /s /q /f .\src\backend\*.egg-info -and \
	del /s /q /f .\*pyc -and \
	del /s /q /f .\*~
else
	rm -rf src/backend/*.egg-info &
	find . -type f -name \*~ | xargs rm &
	find . -type f -name \*pyc | xargs rm
endif

BACKEND_SERVICE := expungeservice
FRONTEND_SERVICE := node
DB_SERVICE := postgres

# currently, only used for PGDATABASE var in 'dropdb' target
include config/postgres/client.env

# one step target for a new dev env
new: up
	@echo waiting for database...
	@sleep 10
	@make initdb

# pulls the necessary images for the local dev services
pull:
	docker-compose pull

# pushes the dev image for the local expungeservice service
push:
	docker-compose push $(BACKEND_SERVICE)

# pulls, then fires up local dev services
up: pull
	docker-compose up -d

# brings down local dev services
down:
	docker-compose down

# runs database initialization scripts - run at first creation or if database
# data volume is removed
initdb:
	docker-compose exec --user=postgres $(DB_SERVICE) /var/lib/postgresql/config/initdb/init-db.dev.sh

# drop database
dropdb:
	docker-compose exec --user=postgres $(DB_SERVICE) sh -l -c "dropdb $(PGDATABASE)"

# run all tests
test: frontend_test_no_watch backend_test

# wipeout containers and volumes
clobber:
	docker-compose down -v

# build expungeservice:dev image
backend_build:
	docker-compose build $(BACKEND_SERVICE)

# tail logs from backend
backend_logs:
	docker-compose logs -f $(BACKEND_SERVICE)

# recreate the backend container; n.b. does not recreate image
backend_reload:
	docker-compose stop $(BACKEND_SERVICE)
	docker rm recordexpungpdx_$(BACKEND_SERVICE)_1
	docker-compose up -d $(BACKEND_SERVICE)

# run backend tests
backend_test:
	docker-compose exec $(BACKEND_SERVICE) pipenv run mypy
	docker-compose exec $(BACKEND_SERVICE) pipenv run pytest

# run react-scripts build
frontend_build: frontend_clean
	@echo `pwd`
	docker run --rm \
		-v `pwd`/src/frontend:/src/frontend \
		-v recordexpungpdx_node_modules:/src/frontend/node_modules \
		node:13.13.0-alpine /bin/sh -c 'cd /src/frontend && ls -al && npm i && npm run build'

# delete react built files
frontend_clean:
	rm -rf src/frontend/build/*

# stop and remove the frontend container
frontend_down:
	docker-compose stop $(FRONTEND_SERVICE)
	docker rm recordexpungpdx_$(FRONTEND_SERVICE)_1

# tail logs from frontend
frontend_logs:
	docker-compose logs -f $(FRONTEND_SERVICE)

# restart frontend
frontend_restart:
	docker-compose restart $(FRONTEND_SERVICE)

# run frontend tests, watching enabled (default)
frontend_test:
	docker-compose exec $(FRONTEND_SERVICE) sh -c 'cd /src/frontend && npm test'

# run frontend tests without watching enabled
frontend_test_no_watch:
	docker-compose exec $(FRONTEND_SERVICE) sh -c 'cd /src/frontend && CI=true npm test'

# pull a database backup from production
#
# expects:
#   * 'Host recordsponge' section in _local_ ~/.ssh/config (see /src/ops/README.md#SSH_Config)
#   * 'prod.env' with database credentials and TIER in _remote_ /etc/recordsponge/
#
prod_db_sync:
	@ssh recordsponge -C \
		'docker pull postgres:10-alpine; \
		 docker run --rm --user=`id -u` --env-file /etc/recordsponge/prod.env --name backup -v /var/tmp:/var/tmp postgres:10-alpine pg_dump -Fc -f /var/tmp/backup-prod.psql'
	@scp recordsponge:/var/tmp/backup-prod.psql config/postgres/backup-prod.psql
	@make dropdb
	@docker-compose exec --user=postgres $(DB_SERVICE) sh -l -c "createdb $(PGDATABASE) && pg_restore -O -d $(PGDATABASE) /var/lib/postgresql/config/backup-prod.psql"
	@rm config/postgres/backup-prod.psql
	@ssh recordsponge -C 'rm /var/tmp/backup-prod.psql'
