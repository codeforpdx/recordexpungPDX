# RecordSponge
[![Build Status](https://travis-ci.com/codeforpdx/recordexpungPDX.svg?branch=master)](https://travis-ci.com/codeforpdx/recordexpungPDX)

A project to automate expunging qualifying criminal records. This project is done in conjunction with Qiu-Qiu Law. [Learn more in the wiki](https://github.com/codeforpdx/recordexpungPDX/wiki).

Please read our [code of conduct](http://www.codeforpdx.org/about/conduct).

If you're interested in learning more about our project and getting involved, please join us at one of our [meetup events!](https://www.meetup.com/Code-for-PDX/) You can also request an invite to join our [Slack channel](https://codeforpdx.slack.com/#record_expung) by contacting our CodeForPDX brigade leader, Hugh: Hugh@codeforpdx.org

## Table of Contents
- [Tech Overview](#tech-overview)
- [Installation](#installation)
- [Running Components](#running-the-docker-stack)
- [Testing](#testing)
- [Contributing](#contributing)
- [Technical Documentation](#technical-documentation)
- [License](#license)

## Tech Overview

This is a web app built using [React](https://reactjs.org/) for the in-browser interface, and a backend web service implemented with the [Flask](https://palletsprojects.com/p/flask/) web framework in Python. The backend app connects to a [Postgres database](https://www.postgresql.org/).

**Our dev environment** is entirely containerized with Docker, and no other dependencies need to be installed natively. We use Python's [pipenv](https://docs.pipenv.org/en/latest/) for maintaining backend dependencies. We use [mypy](http://mypy-lang.org/) to type check any optional typings and [pytest](https://pytest.org/en/latest/) to test backend code. We use [NPM](https://www.npmjs.com/) to develop and build the frontend code. Docker is used to build and deploy the app stack for both local development and for deployment to the web. A postgres database runs as a service within the docker stack, which exposes a connection locally for development and testing.

## Installation

You can get your dev environment up and running with installing only Docker and docker-compose. The npm and backend dev servers run in docker containers, synced with source code directories so that code changes propagate on the local servers right away. If you have any trouble, don't hesitate to ask on our [Slack channel](https://codeforpdx.slack.com/#record_expung)!

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

In the project's root directory, run `make dev_up`. This builds the dev version of the docker images and launches the containers using docker-compose. Stop the running stack with `make dev_down`.

After running `make dev_up`, you can navigate to `localhost` in the browser and see the frontend running.  You can now log in using either of the following credentials

* Email: admin@email.com, Password: admin
* Email: user@email.com, Password: user

If you run `docker ps`, you can see the frontend app running on `localhost:3000`, however if you try logging into this instance instead of the frontend at `localhost`, you will get a 500 server error.

Whenever a dependency is added to the frontend or backend, you will need to rebuild the docker images or you will get errors when trying to run the stack. To do so, take down the stack, rebuild, and restart stack with:
```
make dev_down
make dev_build
make dev_up
```

For more project documentation on Docker, some troubleshooting, and some basic commands, see:
[doc/docker.md](https://github.com/codeforpdx/recordexpungPDX/blob/master/doc/docker.md)

##### Cleaning

While in the directory of your local repo, run:

```
$ make clean
```
in order to remove build artifacts.


## Testing

Currently using [pytest](https://docs.pytest.org) for testing the backend.
Run all tests by running the following command in the project root directory:

```
$ make dev_test
```

This runs a `pytest` command to execute all the unit tests inside the backend docker container. All of these tests should pass if you have correctly set up the backend dev environment.

There are also make targets to operate in a docker container interactively:

```
make bash_backend
```

or

```
make bash_frontend
```


which opens a bash shell inside the respective container. In the backend container, you can then run the python interactive shell with `python3`, or run `pytest`.

To run a subset of test cases without first shelling into the docker container, you can use a docker `exec` command, which specifies a container by name and a runnable command in the container in a single step, e.g.:

```
docker exec -t expungeservice pytest ./tests/[subdir]
```

To specify and run a subset of the test cases.

## Contributing

Please see [CONTRIBUTING.md](CONTRIBUTING.md)

## Technical Documentation

 - Project technical design: [doc/design.md](doc/design.md)
 - Additional frontend docs, mostly design patterns: [src/frontend/README.md](src/frontend/README.md).
 - Some support docs for doing development:
   - [doc/development.md](doc/development.md)

## License

This project is open source under the terms of the [MIT License](LICENSE.md).
