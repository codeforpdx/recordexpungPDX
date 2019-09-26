

api:
	echo $@
	mkdir ./build
	cp -r ../src/backend/expungeservice ./build/expungeservice

	heroku container:push --recursive --app=recordexpungpdxapi
	heroku container:release web --app=recordexpungpdxapi
	rm -rf ./build

frontend:
	echo $@
	mkdir ./build
	cp -r ../config/nginx/* ./build
	cp -r ../src/frontend ./build/frontend

	heroku container:push --recursive --app=recordexpungpdx
	heroku container:release web --app=recordexpungpdx
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
