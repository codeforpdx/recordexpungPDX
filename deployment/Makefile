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
	cp -r ../config/nginx/* ./build/
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
