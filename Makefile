.PHONY: install run clean

install:
	pipenv install '-e .'

run: install
	pipenv run flask run

clean:
	find . -type f -name \*~ | xargs rm
	find . -type f -name \*pyc | xargs rm
	rm -rf src/backend/*.egg-info

IMAGES := database_image

STACK_NAME := recordexpungpdx
DB_NAME := record_expunge
DB_CONTAINER_NAME := db
dev: dev_deploy
	echo $@

dev_deploy: $(IMAGES)
	echo $@
	docker stack deploy -c docker-compose.yml $(STACK_NAME)

dev_stop:
	echo $@
	docker stack rm $(STACK_NAME)

dev_psql:
	docker exec -ti $$(docker ps -qf name=$(DB_CONTAINER_NAME)) psql -U postgres -d $(DB_NAME)

database_image:
	echo $@
	docker build --no-cache -t $(STACK_NAME):database config/postgres

dblogs:
	docker logs --details -ft $$(docker ps -qf name=$(DB_CONTAINER_NAME))
test:
	pipenv run pytest
