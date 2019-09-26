Record Expunge Docker Setup
===========================

Documentation
-------------

[Docker Tutorial](https://docs.docker.com/get-started/)


Containers
----------

We will have three containers: a container for the web server and webapp; a container for the database; and a container for our service.

Each container will have a Dockerfile that describes the container's contents. For conveninence any complex/multi-part command will have a shorter Make target.

We will have two configurations:

- `dev` for development
- `prod` for production

`dev` and `prod` containers will run concurrently, with each `webserver` and `database` containers running on distinct ports. This will allow us to deploy both to the production server and run tests w/o impacting the production database.


**Web Server Container**

This container will run the Nginx web server, which serves the static frontend pages, and forwards api calls to the backend service.


**Database Container**

This container will run the PostgreSQL database.


**Service Container**

This container will run the Python/Flask backend.


Running the containers
----------------------

Development of component source code should often be possible without touching Dockerfiles, so here are a few useful commands that might be sufficient for running and updating docker images in the dev environment.

Do this once:

        docker swarm init

This command designates your system as a "swarm manager" so that it can interact with other nodes in a network. We don't work with multiple nodes in our dev environment, but the command is required to deploy and run a docker stack locally. If your setup has multiple IP addresses e.g. if you are running a linux VM in Windows, you will need to include the --advertise-addr option. More information here: https://docs.docker.com/v17.09/engine/reference/commandline/swarm_init

Below are several docker commands for managing the local docker stack, including rebuilding and restarting the entire stack or its individual images. All make commands need to be executed in the project main folder (the relative location of your Makefile).

1. To build and start the containers, do:

        make dev


This builds the docker images that contain the different app components, then launches the docker stack by instantiating a docker service (which wraps one or more replicated containers) from each component image. While the dev stack is running, each service is accessible in the dev environment at `localhost:<port>`, at the exposed ports defined in the docker-compose.dev.yml file.

Take a look at the Makefile to see all the steps in this make target. You can run these steps individually using the additional make targets provided.

2. To see which containers are running (and with the optional flag to see stopped containers also):

        docker ps [-a]

 **Note:** docker commands and make targets that launch or stop running the containers may return immediately, but take several seconds to take effect. `docker ps` is super useful for this!

3. Individual targets in the Makefile exist for building each docker image. If making local changes to a single component, you can propagate them to the docker stack by first rebuilding the image with:

        make <image_name>


And then restarting the service to run with the new image:

        docker service update --force $(docker stack services ls -f name=CONTAINER_NAME)


4. While the docker stack is running, it will restart any stopped containers automatically using the most recently built image. To stop and restart the entire stack, use the commands

        make dev_stop
        make dev

Note: the `dev_deploy` target rebuilds every image in the stack which may be time-consuming and not necessary if only updating a single image/service. To start a new docker stack without rebuilding the images, use:

        make dev_stop
        make dev_start

5. To stop a single *service* in the running stack, run:

        docker service rm recordexpungpdx_*

replacing * with the service name e.g.  webserver or expungeservice. This stops the corresponding docker container and also prevents the docker orchestrator from spinning up a replacement container. This is useful if you want to, for example, run the node server for frontend development, since the node daemon automatically and rapidly propagates source code changes. 

6. To explore the database:

        make dev_psql


7. To drop the database by removing the database volume:

        make dev_stop
        make dev_drop_database


Reading
-------

[Getting Started -- Docker on Mac OS X](https://medium.com/allenhwkim/getting-started-docker-on-mac-os-x-72c64670464a)

[Get started with Docker for Mac](https://docs.docker.com/docker-for-mac/)
