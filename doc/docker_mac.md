Record Expunge Docker Setup
===========================


Installing on Mac
-----------------

Follow installation instructions in:

    [Getting Started -- Docker on Mac OS X](https://medium.com/allenhwkim/getting-started-docker-on-mac-os-x-72c64670464a)

(click on `Get Docker for Mac [Stable])


Installing on Linux
-------------------

TBD


Containers
----------

We will have three containers: a container for the web server and webapp; a container for the database; and a container for our service.

Each container will have a Dockerfile that describes the container's contents. As a group the containers will be managed with `docker swarm`. For conveninence any complex/multi-part command will have a shorter Make target.

We will have two configurations:

- `dev` for development
- `prod` for production

`dev` and `prod` containers will run concurrently, with each `webserver` and `database` containers running on distinct ports. This will allow us to deploy both to the production server and run tests w/o impacting the production database.


**Web Server Container**

This container will run the Nginx web server and our application.


**Database Container**

This container will run the PostgreSQL database.


**Service Container**

This container will run our Flask service.


Running the containers
----------------------

Do this once:

    docker swarm init

To start the containers, do:

    make dev


To see which containers are running:

    docker ps


To restart a single container:

    docker service update --force $(docker stack services ls -f name=CONTAINER_NAME)


To stop the containers:

    make dev_stop


Reading
-------

[Getting Started -- Docker on Mac OS X](https://medium.com/allenhwkim/getting-started-docker-on-mac-os-x-72c64670464a)
[Get started with Docker for Mac](https://docs.docker.com/docker-for-mac/)
