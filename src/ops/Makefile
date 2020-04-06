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

# echo out version.json
version:
	echo {\"recordexpungPDX\":\"$$(git rev-parse HEAD)\"} > docker/expungeservice/frontend/build/version.json

# build an expungeservice image with the given RS_ENV tag ('staging', 'prod', etc)
image: rsync env_check
	cd docker/expungeservice; \
		docker build . -t recordsponge/expungeservice:$(RS_ENV)

# push expungeservice image with the given RS_ENV tag to hub.docker.com
push: env_check
	docker push recordsponge/expungeservice:$(RS_ENV)

# --- staging

# build staging image
staging_image:
	@make clean
	@cd ../..; make frontend_build
	@make rsync version image RS_ENV=staging

staging_push:
	@make push RS_ENV=staging

# perform staging deploy
#
# expects:
#   * 'Host recordsponge' section in ~/.ssh/config
#   * 'staging.env' with database credentials and TIER in remote home dir
ssh_staging_deploy:
	@ssh recordsponge -C \
		'docker pull recordsponge/expungeservice:staging; \
		 docker stop staging; \
		 docker run --rm -d --name staging --env-file staging.env -p 3032:5000 recordsponge/expungeservice:staging'

# build and deploy staging
staging: staging_image staging_push ssh_staging_deploy
