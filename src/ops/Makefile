# make sure RS_ENV is set and not 'dev'
env_check:
ifndef RS_ENV
	@echo error: RS_ENV value required 1>&2
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
	echo "{\"recordexpungPDX\":\"$$(git rev-parse HEAD)\",\"branch\":\"$$(git rev-parse --abbrev-ref HEAD)\"}" \
		> docker/expungeservice/frontend/build/version.json

# build an expungeservice image with the given RS_ENV tag ('staging', 'prod', etc)
image: rsync env_check
	cd docker/expungeservice; \
		docker build . -t recordsponge/expungeservice:$(RS_ENV)

# push expungeservice image with the given RS_ENV tag to hub.docker.com
push: env_check
	docker push recordsponge/expungeservice:$(RS_ENV)

# --- deploys

# configure port & syslog facility
ifeq ($(RS_ENV),staging)
PORT := 3032
FACILITY := local1
else ifeq ($(RS_ENV),prod)
PORT := 3031
FACILITY := local0
endif

# configure DEPLOY_TAG
ifndef DEPLOY_TAG
DEPLOY_TAG := $(RS_ENV)
endif

# validate PORT setting
port_check:
ifndef PORT
	@echo error: PORT value required - default for '$(RS_ENV)' not found 1>&2
	@exit 1
endif

# ssh to digitalocean host and perform deploy.
#
#   * name of container based on RS_ENV e.g. 'staging' or 'prod'
#   * PORT determined by RS_ENV, override on command line
#   * DEPLOY_TAG defaults to RS_ENV, override on command line
#
# expects:
#   * 'Host recordsponge' section in _local_ ~/.ssh/config (see /src/ops/README.md#SSH_Config)
#   * '*.env' with TIER in _remote_ /etc/recordsponge/
#
ssh_deploy: env_check port_check
	@ssh recordsponge -C \
		'docker pull recordsponge/expungeservice:$(DEPLOY_TAG); \
		 docker rm -f $(RS_ENV) || true; \
		 docker run --rm -d \
		            --name $(RS_ENV) \
								--env-file /etc/recordsponge/$(RS_ENV).env \
								-p $(PORT):5000 \
								--log-driver syslog \
								--log-opt syslog-facility=$(FACILITY) \
								--log-opt tag=$(RS_ENV) \
								recordsponge/expungeservice:$(DEPLOY_TAG)'

# --- staging

# build staging image
staging_image: clean
	@cd ../..; make frontend_build
	@make rsync version image RS_ENV=staging

staging_push:
	@make push RS_ENV=staging

# build and deploy staging
staging: staging_image staging_push
	@make ssh_deploy RS_ENV=staging

# --- production

# build prod image
prod_image: clean
	@cd ../..; make frontend_build
	@make rsync version image RS_ENV=prod

prod_push:
	@make push RS_ENV=prod

# build and deploy prod
prod: prod_image prod_push
	@make ssh_deploy RS_ENV=prod
