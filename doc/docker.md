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

To build and start the containers, do:

    make dev


This builds the docker images that contain the different app components, then launches the docker stack by instantiating a docker service (which wraps one or more replicated containers) from each component image. While the dev stack is running, each service is accessible in the dev environment at `localhost:<port>`, at the exposed ports defined in the docker-compose.dev.yml file.

Take a look at the Makefile to see all the steps in this make target. You can run these steps individually using the additional make targets provided.

To see which containers are running:

    docker ps


Individual targets in the Makefile exist for building each docker image. If making local changes to a single component, you can propagate them to the docker stack by first rebuilding the image with:

    make <image_name>


And then restarting the service to run with the new image:

    docker service update --force $(docker stack services ls -f name=CONTAINER_NAME)


While the docker stack is running, it will restart any stopped containers automatically using the most recently built image. To stop and restart the entire stack, use the commands

    make dev_stop
    make dev_deploy

Note: the `dev_deploy` target rebuilds every image in the stack which may be time-consuming and not necessary if only updating a single image/service. To start a new docker stack without rebuilding the images, use:

    make dev_start


To explore the database:

    make dev_psql


To drop the database by removing the database volume:

    make dev_stop
    make dev_drop_database


Reading
-------

[Getting Started -- Docker on Mac OS X](https://medium.com/allenhwkim/getting-started-docker-on-mac-os-x-72c64670464a)
[Get started with Docker for Mac](https://docs.docker.com/docker-for-mac/)
