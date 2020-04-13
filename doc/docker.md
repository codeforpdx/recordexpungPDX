Record Expunge Docker Setup
===========================

Our project uses Docker to containerize a local dev environment and for deploying the app to production. This document describes the general setup for local dev, staging, and production.

General Documentation
---------------------

[Docker Tutorial](https://docs.docker.com/get-started/)

Dev Environment Containers
--------------------------

There are three services configured in [/docker-compose.yml](/docker-compose.yml), and managed using docker-compose. The project's main [README.md](../README.md) includes the commands to manage the containers locally.

 - **node** react-scripts/webpack dev server (port 3000)
 - **expungeservice** uwsgi server hosting Flask [app](../src/backend/expungservice/app.py) (port 5000)
 - **postgres** postgres database

Named Docker volumes provide persistent storage of database and node\_modules files. To update node dependencies, edit [package.json](../src/frontend/package.json), and restart the container with `make frontend_restart`. Use `make frontend_logs` to watch the NPM install output, and use CTRL-C to stop watching once you see something like:

```
node_1            | You can now view record-expunge-pdx in the browser.
node_1            | 
node_1            |   Local:            http://localhost:3000/
node_1            |   On Your Network:  http://192.168.80.4:3000/
node_1            | 
node_1            | Note that the development build is not optimized.
node_1            | To create a production build, use npm run build.
```

Testing Locally
---------------

Running tests either frontend and backend requires the respective container to be "up". Use the following make targets to run tests:

| target | description |
|-|-|
| test | run both frontend (no watch) and backend tests |
| frontend\_test | run frontend tests in the node container in "watch" mode |
| frontend\_test\_no\_watch | run frontend tests in the node container and exit |

Testing on Pull Request via GitHub Actions (CI)
-----------------------------------------------

We run a continuous integregation testing via [GitHub Actions](https://github.com/features/actions). This both frontend and backend tests, via the same image tags as used in development.

See [main.yml](../.github/workflows/main.yml)

Staging/Prod Environment Containers
-----------------------------------

See [DevOps README](../src/ops/README.md)

Running the Dev containers
--------------------------

Launch the docker-compose services with:

```
make up
```

The services are specified in the file [`docker-compose.yml`](../docker-compose.yml). This target first pulls the dev-tagged docker image, and official images for postgres and ndoe. It then creates and launches a new docker container for each service. It runs the docker stack in detached mode, so you can follow the set of container logs with `docker-compose logs`, or each specific one with `make backend_logs` or `make frontend_logs`. `make backend_build` will build the image `recordsponge/expungeservice:dev` if it can't pull or python dependencies change.

Stop the running containers with:

```
make down
```

To force a rebuild of the expungeservice docker image (if you change any package dependencies), use:

```
make backend_build
```

While the full dev stack is running, you can use the app in two different ways:

#### Frontend Development

The frontend stack uses [react-scripts](https://github.com/facebook/create-react-app#readme) which starts a hot-module-reloading dev server for quick iterative work. This is run inside the `node` service, which runs from the stock `node:alpine` image and mounts a persistent named volume to house the node\_modules. This service is listening at:

[http://localhost:3000](http://localhost:3000)

The dev server is configured to proxy the backend API endpoints, so having the backend service running is required. Check out the [make targets](../Makefile) beginning with `frontend_` for commented details.

In the case that one needs to blow away the node\_modules tree and reinstall, use the following steps:

1. `make frontend_down`
2. `docker volume rm recordexpungpdx_node_modules`
3. `make up`
4. `make frontend_logs` to watch install output, ctrl-c when done.

NOTE: a staging/prod deploy uses the output from `npm run build` and does not run any node service.

#### Backend Development

The backend stack uses a Docker Hub published image `recordsponge/expungeservice` with the `:dev` tag. This runs a reloading [uwsgi](https://uwsgi-docs.readthedocs.io/en/latest/) server, handling the [Flask](https://flask.palletsprojects.com/en/1.1.x/) app at [app.py](../src/backend/expungeservice/app.py). This service is listening at:

[http://localhost:5000](http://localhost:5000)

The uwsgi server is run with `--py-autoreload`, so it will hot reload on detected source file chnages. The local `src/backend` and `src/frontend` trees are bind mounted into the container. Frontend source is in there so the Flask app can serve static files out of `src/frontend/build`, where an `npm run build` command would produce deployable artifacts. Check out the [make targets](../Makefile) beginning with `backend_` for commented details.

Some CLI commands
-----------------

To see which containers are running (and with the optional flag to see stopped containers also):


        docker-compose ps


To start a PostgreSQL interactive terminal to access the database:

        docker-compose exec --user=postgres postgres psql record_expunge_dev

Exit the psql terminal with `\q`.

More Reading
------------

[Getting Started -- Docker on Mac OS X](https://medium.com/allenhwkim/getting-started-docker-on-mac-os-x-72c64670464a)

[Get started with Docker for Mac](https://docs.docker.com/docker-for-mac/)
