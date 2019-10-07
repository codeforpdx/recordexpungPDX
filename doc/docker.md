Record Expunge Docker Setup
===========================

Our project uses Docker to containerize a local dev environment and for deploying the app to production. This document describes the general setup for each of our three environments: dev (local), test (travis-ci), and prod (heroku).

General Documentation
---------------------

[Docker Tutorial](https://docs.docker.com/get-started/)



Dev Environment Containers
--------------------------

There are four containers which are configured in /docker-compose.dev.yml , and managed using docker-compose. The project's main README.md includes the commands to manage the containers locally.

 - **webserver** webpack dev server
 - **expungeservice** wsgi server (hosting a Flask app)
 - **db** postgres database
 - **nginx** proxies /api/ paths to the backend and everything else to the frontend.

Docker volumes sync the project's source code directories with the frontend and backend dev servers, so that the containers don't need to be rebuilt to reflect code changes, only new package dependencies.

Test Environment Containers
---------------------------

We run a continuous integregation testing pipe using [Travis CI](https://travis-ci.com/). This runs three containers which are managed in the docker-compose.test.yml file.

 - **webserver** nginx server that contains the frontend static files, built with webpack
 - **expungeservice** wsgi server (hosting a Flask app)
 - **db** postgres database

Prod Environment Containers
---------------------------

The app is deployed to Heroku in just two containers, each served from a standalone Heroku app:

 - **webserver** The frontend is an nginx container that serves the static files, and proxies api requests to the backend. It runs at https://recordexpungpdx.herokuapp.com/
 - **expungeservice** The backend is a wsgi server that runs at https://recordexpungpdxapi.herokuapp.com/

The database runs in a heroku-postgres plugin that is attached to the backend.

Dockerfiles
-----------

Some variations exist between the Dockerfiles used for each enviroment. TODO: elaborate on this a little bit.

 - The biggest difference between `dev` and the other environments is that in `dev`, npm runs a webpack server to serve frontend files, whereas in `test` and `prob` the static web files are generated when the nginx image is built and then served by nginx.
 - The nginx `conf` file has some differences for each, because the respective servers ... need

Running the Dev containers
--------------------------

Launching and managing the local workspace uses a few commands written in the project's Makefile:

Launch the docker containers with:

```
make dev_up
```

This follows a few steps specified in the file `docker-compose.dev.yml`. It first builds the dev docker images using the named Dockerfiles if those images don't already exist. It then creates and launches a new docker container for each service. It runs the docker stack in detached mode, so you can follow the set of container logs with:

```
make dev_logs
```

While the dev stack is running, the integrated app (frontend and backend) is accessible at `http://localhost`. This port (80 is the default for http) is exposed by the nginx container, which proxies calls to the backend (any paths of the form `/api/*`) or to the frontend (any other paths).

The docker-compose file also exposes the frontend, backend, and database each at their own port, so you can access each directly, e.g. if you want to connect to the database by running `psql` locally. Note that accessing the frontend at its own port causes its requests to the backend to fail, because they aren't going through the nginx server.

Stop the running containers with

```
make dev_down
```

To force a rebuild of the docker images (if you change any package dependencies), use

```
make dev_build
```

Some CLI commands
-----------------

To see which containers are running (and with the optional flag to see stopped containers also):


        docker ps [-a]


To start a PostgreSQL interactive terminal to access the database:

        make dev_psql

Exit the psql terminal with `\q`.

Running the Test containers
---------------------------

Because of the differences between the `dev` and `test` stacks, a different set of Dockerfiles and commands are used to build and run the test containers. You can do this for local testing as well as with the automated scripts on Travis. The deployment uses `docker stack` commands rather than `docker-compose`. This is worth changing -- `docker stack` is good for doin more powerful container orchestration than with docker-compose, but we don't really need it for any part of our project.

If you want to play around with some of our deprecated Docker features a bit more, here is the defunct documentation:

Do this once:


        docker swarm init


This command designates your system as a "swarm manager" so that it can interact with other nodes in a network. We don't work with multiple nodes in our dev environment, but the command is required to deploy and run the docker test stack locally. If your setup has multiple IP addresses e.g. if you are running a linux VM in Windows, you will need to include the --advertise-addr option. More information here: https://docs.docker.com/v17.09/engine/reference/commandline/swarm_init

Below are several docker commands for managing the local docker stack, including rebuilding and restarting the entire stack or its individual images. All make commands need to be executed in the project main folder (the relative location of your Makefile).

1. To build and start the containers, do:


        make dev_deploy


This builds the docker images that contain the different app components, then launches the docker stack by instantiating a docker service (which wraps one or more replicated containers) from each component image.

Take a look at the Makefile to see all the steps in this make target. You can run these steps individually using the additional make targets provided. It may also be useful to check out what the `make` targets from the Makefile are doing.


 **Note:**  `docker stack` commands and make targets that launch or stop running the stack containers may return immediately, but take several seconds to take effect. `docker ps` is super useful for this!

2. Individual targets in the Makefile exist for building each docker image. If making local changes to a single component, you can propagate them to the docker stack by first rebuilding the image with:


        make <image_name>


And then restarting the service to run with the new image:


        docker service update --force $(docker stack services ls -f name=CONTAINER_NAME)


3. While the docker stack is running, it will restart any stopped containers automatically using the most recently built image. To stop and restart the entire stack, use the commands

        make dev_stop
        make dev_deploy

Note: the `dev_deploy` target rebuilds every image in the stack which may be time-consuming and not necessary if only updating a single image/service. To start a new docker stack without rebuilding the images, use:

        make dev_stop
        make dev_start

4. To stop a single *service* in the running stack, run:

        docker service rm recordexpungpdx_*

replacing * with the service name e.g.  webserver or expungeservice. This stops the corresponding docker container and also prevents the docker orchestrator from spinning up a replacement container.

5. To drop the test database by removing the database volume:

        make dev_stop
        make dev_drop_database


More Reading
------------

[Getting Started -- Docker on Mac OS X](https://medium.com/allenhwkim/getting-started-docker-on-mac-os-x-72c64670464a)

[Get started with Docker for Mac](https://docs.docker.com/docker-for-mac/)
