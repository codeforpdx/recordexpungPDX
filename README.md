# RecordSponge
![](https://github.com/codeforpdx/recordexpungPDX/workflows/recordexpungPDX%20tests/badge.svg)

A project to automate expunging qualifying criminal records. This project is done in conjunction with Qiu-Qiu Law. [Learn more in the wiki](https://github.com/codeforpdx/recordexpungPDX/wiki).

This software is mature and currently has a sole maintainer, and doesn't need any further contributions.

To connect with the creator community, come to one of our [meetup events!](https://www.meetup.com/Code-for-PDX/)

## Table of Contents
- [Tech Overview](#tech-overview)
- [Installation](#installation)
- [Running Components](#running-the-docker-stack)
- [Testing](#testing)
- [Contributing](#contributing)
- [Technical Documentation](#technical-documentation)
- [License](#license)

## Tech Overview

This is a web app built using [React](https://reactjs.org/) for the in-browser interface, and a backend web service implemented with the [Flask](https://palletsprojects.com/p/flask/) web framework in Python.

**Our dev environment** is entirely containerized with Docker, and no other dependencies need to be installed natively. We use Python's [pipenv](https://docs.pipenv.org/en/latest/) for maintaining backend dependencies. We use [mypy](http://mypy-lang.org/) to type check any optional typings and [pytest](https://pytest.org/en/latest/) to test backend code. We use [NPM](https://www.npmjs.com/) to develop and build the frontend code. Docker is used to build and deploy the app stack for both local development and for deployment to the web.

## Installation

You can get your dev environment up and running with installing only Docker and docker-compose. The npm and backend dev servers run in docker containers, synced with source code directories so that code changes propagate on the local servers right away.

1. **[Fork](https://help.github.com/articles/fork-a-repo/#fork-an-example-repository)** the repo to create a copy for your own github account,
  and **[clone](https://help.github.com/articles/fork-a-repo/#step-2-create-a-local-clone-of-your-fork)** your own copy. (Read [CONTRIBUTING.md](CONTRIBUTING.md) for important info about syncing code your on github) 


2. Install docker

   * **Mac**

        - Follow installation instructions in: [Getting Started -- Docker on Mac OS X](https://medium.com/allenhwkim/getting-started-docker-on-mac-os-x-72c64670464a)

          (click on Get Docker for Mac [Stable])

   * **Linux**

        - First, follow: [Docker Installation](https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-using-the-repository)

        - Configure your user to run docker without sudo: https://docs.docker.com/install/linux/linux-postinstall/
        
        - Install [docker-compose](https://docs.docker.com/compose/install/)

   * **Windows**
        - Windows (as always) is a bit more challenging. Docker CE on Windows requires Hyper-V support, which is only available on Windows 10 Pro, Enterprise, or Education.
        If you have one of those versions, follow [Docker's documentation to install Docker Engine](https://docs.docker.com/docker-for-windows/install/).
        - **If you have Hyper-V**:
            - Install GNU Make for Windows using either [Chocolatey](https://chocolatey.org/) or by downloading the executable
        [from sourceforge](http://gnuwin32.sourceforge.net/packages/make.htm), running the installer, and then putting the 
        binary on your [Path Environment variable](https://helpdeskgeek.com/windows-10/add-windows-path-environment-variable/).
        - **If you have Windows 10 Community, Home, or other versions**, [create a Linux VM using VirtualBox and run Docker Engine](https://www.sitepoint.com/docker-windows-10-home/) 
        through there.  Alternately, you could partition your hard drive [and dual-boot Linux to use for development](https://opensource.com/article/18/5/dual-boot-linux).
        -   ##### Important Windows Note 
            if your git config changes [Linux-style line endings into windows-style line endings](http://www.cs.toronto.edu/~krueger/csc209h/tut/line-endings.html)
            using the `core.autocrlf` config flag, you'll need to disable that in order for the docker builds to work 
            correctly.  You can disable this setting for just the `recordexpungPDX` repo by running `git config --local core.autocrlf false`
            from the root directory of this repo.

## Running the docker stack

In the project's root directory, run `make new`. This pulls the dev-tagged "expungeservice" image and launches the containers using docker-compose. Start and stop the running stack with `make up` and `make down`.

After this target completes, you can navigate to [http://localhost:3000](http://localhost:3000) in the browser and connect to the React dev server with full hot-module reloading. This may take a minute or two to come up before it is available while it installs node modules. Check the service with `make frontend_logs`.

In the course of backend development, one may not need to be running the React/HMR dev server. To build the frontend static files, and use Flask to serve them, run the following command:

```
$ make frontend_down frontend_build
```

Then navigate to [http://localhost:5000](http://localhost:5000) to access the backend service directly. This is configured to serve the static files. `make up` will start the HMR dev server again at 3000 if you stopped it.

Whenever a dependency is added to the backend, someone needs to rebuild the dev-tagged image and push or folks will get errors when trying to run the stack. To do so, rebuild the image, and reload the backend with:

```
$ make backend_build backend_reload
```

If it works, push with:

```
$ make push
```

More details in [DevOps README](src/ops/README.md).

For more project documentation on Docker, some troubleshooting, and some basic commands, see:
[doc/docker.md](https://github.com/codeforpdx/recordexpungPDX/blob/master/doc/docker.md)

##### Cleaning

While in the directory of your local repo, run:

```
$ make clean
```
in order to remove build artifacts.

To completely remove containers, volumes, and compose networks, run:

```
$ make clobber
```

## DevOps

See [DevOps README](src/ops/README.md).

## Testing

Currently using [pytest](https://docs.pytest.org) for testing the backend.
Run all backend tests by running the following command in the project root directory:

```
$ make backend_test
```

This runs a `pytest` command to execute all the unit tests inside the backend docker container. All of these tests should pass if you have correctly set up the backend dev environment.

To run a subset of test cases without first shelling into the docker container, you can use a docker-compose `exec` command, which specifies a container by service name and a runnable command in the container in a single step, e.g.:

```
$ docker-compose exec expungeservice pipenv run pytest tests/[subdir]
```

To specify and run a subset of the test cases.

## Contributing

Please see [CONTRIBUTING.md](CONTRIBUTING.md)

## Technical Documentation

 - Project technical design: [doc/design.md](doc/design.md)
 - Additional frontend docs, mostly design patterns: [src/frontend/README.md](src/frontend/README.md).

## License

This project is open source under the terms of the [MIT License](LICENSE.md).
