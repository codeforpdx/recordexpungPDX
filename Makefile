.PHONY: clean

STACK_NAME := recordexpungpdx
DB_CONTAINER_NAME := db
BACKEND_CONTAINER_NAME := expungeservice
FRONTEND_CONTAINER_NAME := webserver
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

dev: dev_up

dev_up:
	docker-compose -f docker-compose.dev.yml up -d

dev_down:
	docker-compose -f docker-compose.dev.yml down

dev_build:
	docker-compose -f docker-compose.dev.yml build

dev_logs:
	docker-compose -f docker-compose.dev.yml logs -f

dev_psql:
	docker exec -ti $(shell docker ps -qf name=$(DB_CONTAINER_NAME)) psql -U postgres -d record_expunge # TODO: Extract db name from config/expungeservice/expungeservice.env

bash_backend:
	docker exec -it $(shell docker ps -qf name=$(BACKEND_CONTAINER_NAME)) /bin/bash

bash_frontend:
	docker exec -it $(shell docker ps -qf name=$(FRONTEND_CONTAINER_NAME)) /bin/bash

database_image:
	docker build --no-cache -t $(STACK_NAME):database config/postgres -f config/postgres/Dockerfile.dev

expungeservice_image:
	docker build --no-cache -t $(STACK_NAME):expungeservice src/backend/ -f src/backend/Dockerfile.dev

dblogs:
	docker logs --details -ft $(shell docker ps -qf name=$(DB_CONTAINER_NAME))

applogs:
	docker logs --details -ft $(shell docker ps -qf name=$(BACKEND_CONTAINER_NAME))

weblogs:
	docker logs --details -ft $(shell docker ps -qf name=$(FRONTEND_CONTAINER_NAME))

dev_test:
	docker exec -t $(shell docker ps -qf name=$(BACKEND_CONTAINER_NAME)) mypy
	docker exec -t $(shell docker ps -qf name=$(BACKEND_CONTAINER_NAME)) pytest

dev_drop_database:
	docker volume rm $(shell docker volume ls -qf name=$(STACK_NAME))

dev_mock_oeci_up:
	docker-compose -f docker-compose.dev.yml -f src/frontend/developerUtils/docker-compose.mock-oeci.yml up -d

deploy: deploy_backend deploy_frontend

.ONESHELL:
deploy_update_repo:
	cd ~/recordexpungPDX/
	git reset --hard
	git checkout master
	git pull origin master

.ONESHELL:
deploy_backend: deploy_update_repo
	cd ~/recordexpungPDX/src/backend/
	killall uwsgi
	$(shell tr '\n' ' ' < ~/recordexpungPDX/config/expungeservice/expungeservice.production.env) nohup pipenv run uwsgi --socket 127.0.0.1:3031 --module expungeservice.wsgi &

.ONESHELL:
deploy_frontend: deploy_update_repo
	cd ~/recordexpungPDX/src/frontend/
	npm run build
	cp -r build/* /usr/share/nginx/html/

.PHONY: $(REQUIREMENTS_TXT)
$(REQUIREMENTS_TXT):
	pipenv lock -r > $@

# ---

# currently, only used for PGDATABASE var in 'dropdb' target
include config/postgres/client.env

# pulls the necessary images for the local dev services
pull:
	docker-compose pull

# pushes the dev image for the local expungeservice service
push:
	docker-compose push expungeservice

# pulls, then fires up local dev services
up: pull
	docker-compose up -d

# brings down local dev services
down:
	docker-compose down

# runs database initialization scripts - run at first creation or if database
# data volume is removed
initdb:
	docker-compose exec --user=postgres postgres /var/lib/postgresql/config/initdb/init-db.dev.sh

# drop database
dropdb:
	docker-compose exec --user=postgres postgres sh -l -c "dropdb $(PGDATABASE)"

# run all tests
test: frontend_test_no_watch backend_test

# recreate the backend container; n.b. does not recreate image
backend_reload:
	docker-compose stop expungeservice
	docker rm recordexpungpdx_expungeservice_1
	docker-compose up -d expungeservice

# run backend tests
backend_test:
	docker-compose exec expungeservice pipenv run mypy
	docker-compose exec expungeservice pipenv run pytest

# run react-scripts build
frontend_build: frontend_clean
	docker run --rm \
		-v `pwd`/src/frontend:/src/frontend \
		-v recordexpungpdx_node_modules:/src/frontend/node_modules \
		node:alpine /bin/sh -c 'cd /src/frontend && npm run build'

# delete react built files
frontend_clean:
	rm -rf src/frontend/build/*

# stop and remove the frontend container
frontend_down:
	docker-compose stop node
	docker rm recordexpungpdx_node_1

# run frontend tests, watching enabled (default)
frontend_test:
	docker-compose exec node sh -c 'cd /src/frontend && npm test'

# run frontend tests without watching enabled
frontend_test_no_watch:
	docker-compose exec node sh -c 'cd /src/frontend && CI=true npm test'
