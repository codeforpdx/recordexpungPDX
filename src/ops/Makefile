# make sure RS_ENV is set and not 'dev'
env_check:
ifndef RS_ENV
	@echo error: set RS_ENV to 'staging' or 'prod' 1>&2
	@exit 1
endif
ifeq ($(RS_ENV),dev)
	@echo error: RS_ENV can not be set to 'dev' 1>&2
	@exit 1
endif

# remove source from docker image context tree
clean:
	rm -rf docker/expungeservice/backend \
         docker/expungeservice/frontend

# synchronize source trees into docker context tree
rsync:
	rsync -rlptoD --delete --omit-dir-times --exclude logs --exclude flask_session ../backend docker/expungeservice
	rsync -rlptoD --delete --omit-dir-times ../frontend/build docker/expungeservice/frontend

# build an expungeservice image with the given RS_ENV tag ('staging', 'prod', etc)
image: rsync env_check
	cd docker/expungeservice; \
		docker build . -t recordsponge/expungeservice:$(RS_ENV)

# push expungeservice image with the given RS_ENV tag to hub.docker.com
push: env_check
	docker push recordsponge/expungeservice:$(RS_ENV)

# build staging image
staging:
	@make clean
	@cd ../..; make frontend_build
	@make rsync image RS_ENV=staging

# launch staging container, only run on staging deploy host
# expects './staging.env' with database credentials and TIER
staging_deploy:
	@docker pull recordsponge/expungeservice:staging
	@docker stop staging
	docker run --rm -d --name staging -p --env-file staging.env -p 3032:5000 recordsponge/expungeservice:staging
