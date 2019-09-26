.PHONY: install run clean



install:
	pipenv install

clean:
	rm -rf src/backend/*.egg-info
	find . -type f -name \*~ | xargs rm
	find . -type f -name \*pyc | xargs rm

IMAGES := database_image expungeservice_image webserver_image

STACK_NAME := recordexpungpdx
PGDATABASE := record_expunge
DB_CONTAINER_NAME := db
REQUIREMENTS_TXT := src/backend/expungeservice/requirements.txt

dev: dev_up
	echo $@

dev_up:
	echo $@
	docker-compose -f docker-compose.dev.yml up

dev_down:
	echo $@
	docker-compose -f docker-compose.dev.yml down

dev_build:
	echo @
	docker-compose -f docker-compose.dev.yml build

dev_deploy: $(IMAGES) dev_start
	echo $@

dev_start:
	# This restarts the docker stack without rebuilding the underlying docker images;
	# to reflect  code changes in the new stack you'll need to rebuild the altered image(s)
	# with the appropriate make target,
	# or with `make dev` which rebuilds all three images.

	echo $@
	docker stack deploy -c docker-compose.dev.yml $(STACK_NAME)

dev_stop:
	echo $@
	docker stack rm $(STACK_NAME)

dev_psql:
	docker exec -ti $$(docker ps -qf name=$(DB_CONTAINER_NAME)) psql -U postgres -d $(PGDATABASE)

database_image:
	docker build --no-cache -t $(STACK_NAME):database config/postgres -f config/postgres/Dockerfile.dev

expungeservice_image:
	docker build --no-cache -t $(STACK_NAME):expungeservice src/backend/expungeservice -f src/backend/expungeservice/Dockerfile.dev

webserver_image:
	cp -r src/frontend/ config/nginx/frontend
	docker build --no-cache -t $(STACK_NAME):webserver config/nginx -f config/nginx/Dockerfile.dev
	rm -rf config/nginx/frontend

dblogs:
	docker logs --details -ft $$(docker ps -qf name=$(DB_CONTAINER_NAME))

applogs:
	docker logs --details -ft $$(docker ps -qf name=expungeservice)

test:
	pipenv run pytest --ignore=src/frontend/

dev_stack_test:
	docker cp ./src/backend/tests/ $$(docker ps -qf name=expungeservice):/var/www/tests
	docker exec -ti $$(docker ps -qf name=expungeservice) touch /var/www/conftest.py
	docker exec -ti $$(docker ps -qf name=expungeservice) pytest

dev_drop_database:
	docker volume rm $$(docker volume ls -qf name=$(STACK_NAME))

.PHONY: $(REQUIREMENTS_TXT)
$(REQUIREMENTS_TXT):
	pipenv lock -r > $@
