handle_error = (rm -rf ./build && exit 1)

api:
	echo $@
	mkdir ./build
	cp -r ../src/backend/ ./build/expungeservice
	# Ensures heroku doesn't unnecessarily build Dockerfile.dev which isn't used for production
	rm ./build/expungeservice/Dockerfile.dev

	heroku container:push --recursive --app=recordexpungpdxapi || $(handle_error)
	heroku container:release web --app=recordexpungpdxapi || $(handle_error)
	rm -rf ./build

frontend:
	echo $@
	mkdir ./build
	cp ../config/nginx/Dockerfile.web ./build/
	cp ../config/nginx/nginx.conf ./build/
	cp ../config/nginx/recordexpunge-nginx.conf ./build/
	rsync -a ../src/frontend/ ./build/frontend/ --exclude node_modules

	heroku container:push --recursive --app=recordexpungpdx || $(handle_error)
	heroku container:release web --app=recordexpungpdx || $(handle_error)
	rm -rf ./build

db:
	echo $@
	# re-deploying the database is tricky because we can't/ don't want to just replace what's there.
	# but here are the commands:

	heroku addons:create heroku-postgresql:hobby-dev --app=recordexpungpdxapi

	#this runs the initialization scripts
	heroku pg:psql --app=recordexpungpdxapi -f ./config/postgres/initdb/scripts/create-tables.sql
	heroku pg:psql --app=recordexpungpdxapi -f ./config/postgres/initdb/scripts/create-functions.sql
	heroku pg:psql --app=recordexpungpdxapi -f ./config/postgres/initdb/scripts/initial_credentials.sql

api_staging:
	echo $@
	mkdir ./build
	cp -r ../src/backend/ ./build/expungeservice
	# Ensures heroku doesn't unnecessarily build Dockerfile.dev which isn't used for production
	rm ./build/expungeservice/Dockerfile.dev

	heroku container:push --recursive --app=recordexpungpdxapi-test || $(handle_error)
	heroku container:release web --app=recordexpungpdxapi-test || $(handle_error)
	rm -rf ./build

frontend_staging:
	echo $@
	mkdir ./build
	cp ../config/nginx/Dockerfile.staging ./build/Dockerfile.web
	cp ../config/nginx/nginx.conf ./build/
	cp ../config/nginx/recordexpunge-nginx.staging.conf ./build/
	rsync -a ../src/frontend/ ./build/frontend/ --exclude node_modules

	heroku container:push --recursive --app=recordexpungpdx-test || $(handle_error)
	heroku container:release web --app=recordexpungpdx-test || $(handle_error)
	rm -rf ./build
