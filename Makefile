.PHONY: install run clean

install:
	pipenv install

clean:
	rm -rf src/backend/*.egg-info
	find . -type f -name \*~ | xargs rm
	find . -type f -name \*pyc | xargs rm

IMAGES := database_image expungeservice_image webserver_image

STACK_NAME := recordexpungpdx
DB_NAME := record_expunge
DB_CONTAINER_NAME := db
REQUIREMENTS_TXT := src/backend/expungeservice/requirements.txt

dev: $(REQUIREMENTS_TXT) dev_deploy
	echo $@

dev_deploy: $(IMAGES) dev_start
	echo $@

dev_start:
	echo $@
	docker stack deploy -c docker-compose.yml -c docker-compose.dev.yml $(STACK_NAME)

dev_stop:
	echo $@
	docker stack rm $(STACK_NAME)

dev_psql:
	docker exec -ti $$(docker ps -qf name=$(DB_CONTAINER_NAME)) psql -U postgres -d $(DB_NAME)

database_image:
	docker build --no-cache -t $(STACK_NAME):database config/postgres

expungeservice_image:
	docker build --no-cache -t $(STACK_NAME):expungeservice src/backend/expungeservice

webserver_image:
	cp -r src/frontend/ config/nginx/frontend
	docker build --no-cache -t $(STACK_NAME):webserver config/nginx
	rm -rf config/nginx/frontend

dblogs:
	docker logs --details -ft $$(docker ps -qf name=$(DB_CONTAINER_NAME))

applogs:
	docker logs --details -ft $$(docker ps -qf name=expungeservice)

test:
	pipenv run pytest --ignore=src/frontend/

dev_drop_database:
	docker volume rm $$(docker volume ls -qf name=$(STACK_NAME))

.PHONY: $(REQUIREMENTS_TXT)
$(REQUIREMENTS_TXT):
	pipenv lock -r > $@
