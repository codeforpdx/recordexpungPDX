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

# one step target for a new dev env
new: up
	@echo TODO: Remove this make target

# pulls the necessary images for the local dev services
pull:
	docker-compose pull

# pushes the dev image for the local expungeservice service to dockerhub
push:
	docker-compose push $(BACKEND_SERVICE)

# pulls, then fires up local dev services
up: pull
	docker-compose up -d

# brings down local dev services
down:
	docker-compose down

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
	docker-compose exec $(BACKEND_SERVICE) pipenv run pytest --cov=expungeservice --cov-report term-missing

# run react-scripts build
frontend_build: frontend_clean
	docker run --rm \
		-v `pwd`/src/frontend:/src/frontend \
		-v recordexpungpdx_node_modules:/src/frontend/node_modules \
		node:13.13.0-alpine /bin/sh -c 'cd /src/frontend && npm i && npm run build'

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
