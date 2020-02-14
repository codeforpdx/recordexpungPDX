.PHONY: clean

STACK_NAME := recordexpungpdx
PGDATABASE := record_expunge
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
ifeq ($(OSFLAG), WIN32)
	docker exec -ti $(shell docker ps -qf name=$(DB_CONTAINER_NAME)) psql -U postgres -d $(PGDATABASE)
else
	docker exec -ti $$(docker ps -qf name=$(DB_CONTAINER_NAME)) psql -U postgres -d $(PGDATABASE)
endif

bash_backend:
ifeq ($(OSFLAG), WIN32)
	docker exec -it $(shell docker ps -qf name=$(BACKEND_CONTAINER_NAME)) /bin/bash
else
	docker exec -it $$(docker ps -qf name=$(BACKEND_CONTAINER_NAME)) /bin/bash
endif

bash_frontend:
ifeq ($(OSFLAG), WIN32)
	docker exec -it $(shell docker ps -qf name=$(FRONTEND_CONTAINER_NAME)) /bin/bash
else
	docker exec -it $$(docker ps -qf name=$(FRONTEND_CONTAINER_NAME)) /bin/bash
endif

dblogs:
ifeq ($(OSFLAG), WIN32)
	docker logs --details -ft $(shell docker ps -qf name=$(DB_CONTAINER_NAME))
else
	docker logs --details -ft $$(docker ps -qf name=$(DB_CONTAINER_NAME))
endif

applogs:
ifeq ($(OSFLAG), WIN32)
	docker logs --details -ft $(shell docker ps -qf name=$(BACKEND_CONTAINER_NAME))
else
	docker logs --details -ft $$(docker ps -qf name=$(BACKEND_CONTAINER_NAME))
endif

weblogs:
ifeq ($(OSFLAG), WIN32)
	docker logs --details -ft $(shell docker ps -qf name=$(FRONTEND_CONTAINER_NAME))
else
	docker logs --details -ft $$(docker ps -qf name=$(FRONTEND_CONTAINER_NAME))
endif

dev_test:
ifeq ($(OSFLAG), WIN32)
	docker exec -t $(shell docker ps -qf name=$(BACKEND_CONTAINER_NAME)) mypy
	docker exec -t $(shell docker ps -qf name=$(BACKEND_CONTAINER_NAME)) pytest
else
	docker exec -t $$(docker ps -qf name=$(BACKEND_CONTAINER_NAME)) mypy
	docker exec -t $$(docker ps -qf name=$(BACKEND_CONTAINER_NAME)) pytest
endif

dev_drop_database:
ifeq ($(OSFLAG), WIN32)
	docker volume rm $(shell docker volume ls -qf name=$(STACK_NAME))
else
	docker volume rm $$(docker volume ls -qf name=$(STACK_NAME))
endif

dev_mock_oeci_up:
	docker-compose -f docker-compose.dev.yml -f src/frontend/developerUtils/docker-compose.mock-oeci.yml up -d

.PHONY: $(REQUIREMENTS_TXT)
$(REQUIREMENTS_TXT):
	pipenv lock -r > $@
