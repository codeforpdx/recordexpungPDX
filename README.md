# recordexpungPDX
A project to automate expunging qualifying criminal records.  This project is done in conjunction with the Multnomah County Public Defender's Office. [Learn more in the wiki](https://github.com/codeforpdx/recordexpungPDX/wiki).

This README is covers project installation and getting started as a contributor. If you're interested in contributing, please join us at one of our meetup events! https://www.meetup.com/Code-for-PDX/ Also here's a short description of how you could help: [doc/contributing.md](https://github.com/codeforpdx/recordexpungPDX/blob/master/doc/contributing.md)


More documentation:
 - Project technical design: [doc/design.md](https://github.com/codeforpdx/recordexpungPDX/blob/master/doc/design.md)
 - Additional frontend docs, mostly design patterns: [src/frontend/README.md](https://github.com/codeforpdx/recordexpungPDX/blob/master/src/frontend/README.md).
 - Some support docs for doing development:
   - [doc/development.md](https://github.com/codeforpdx/recordexpungPDX/blob/master/doc/development.md)
   - Docker usage: [doc/docker.md](https://github.com/codeforpdx/recordexpungPDX/blob/master/doc/docker.md)
   - Mock search.py and oeci_login.py usage: [src/frontend/developerUtils/developerUtils.md](https://github.com/codeforpdx/recordexpungPDX/blob/master/src/frontend/developerUtils/developerUtils.md)

[![Build Status](https://travis-ci.com/codeforpdx/recordexpungPDX.svg?branch=master)](https://travis-ci.com/codeforpdx/recordexpungPDX)

## Table of Contents
- [Tech Overview](#tech-overview)
- [Installation](#installation)
- [Running Components](#running-the-docker-stack)
- [Testing](#testing)
- [Project Layout](#project-layout)
- [Contributing](#contributing)
- [License](#license)

## Tech Overview

This is a web app built using [React](https://reactjs.org/) for the in-browser interface, and a backend web service implemented with the [Flask](https://palletsprojects.com/p/flask/) web framework in Python. The backend app connects to a [Postgres database](https://www.postgresql.org/).

The app is deployed on the free(mium) webapp hosting service, [Heroku](https://www.heroku.com/).

Our latest dev version (this repo's master branch) is publicly viewable! Here: https://recordexpungpdx.herokuapp.com/

**Our dev environment** uses Python's [pipenv](https://docs.pipenv.org/en/latest/) for maintaining backend dependencies, and [pytest](https://pytest.org/en/latest/) to develop backend code. We use [NPM](https://www.npmjs.com/) to develop and build the frontend code. Docker is used to build and deploy the app stack for both local development and for deployment to the web. A postgres database runs as a service within the docker stack, which exposes a connection locally for development and testing.

## Installation

You can get your dev environment up and running with installing only Docker and docker-compose. The npm and backend dev servers run in docker containers, synced with source code directories so that code changes propagate on the local servers right away. If you have any trouble, don't hesitate to ask on our [Slack channel](https://codeforpdx.slack.com/#record_expung)! If you don't have access to the slack channel yet, please ask our CodeForPDX brigade leader, Hugh: Hugh@codeforpdx.org

1. **[Fork](https://help.github.com/articles/fork-a-repo/#fork-an-example-repository)**,
  and **[clone](https://help.github.com/articles/fork-a-repo/#step-2-create-a-local-clone-of-your-fork)** the repo.


2. Install docker

   * **Mac**

        - Follow installation instructions in: [Getting Started -- Docker on Mac OS X](https://medium.com/allenhwkim/getting-started-docker-on-mac-os-x-72c64670464a)

          (click on Get Docker for Mac [Stable])

   * **Linux**

        - First, follow: [Docker Installation](https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-using-the-repository)

        - Configure your user to run docker without sudo: https://docs.docker.com/install/linux/linux-postinstall/

   * **Window**
        - instructions not written. If you use Windows, we'd love your contribution here!

3. Install [docker-compose](https://docs.docker.com/compose/install/)

### Running the docker stack

In the project's root directory, run `make dev_up`. This builds the dev version of the docker images and launches the containers using docker-compose. Stop the running stack with `make dev_down`.

After running `make dev_up`, you can navigate to localhost in the browser and see the frontend running.  You can now log in using either of the following credentials

* Email: admin@email.com, Password: admin
* Email: user@email.com, Password: user

If you run docker ps, you can see a front end running on localhost:3000, however if you try logging while not on just localhost, you will get a 500 server error.



If you need to rebuild the project (for example if you add new dependencies to the frontend or backend services), you can run the `make dev_build` command.

For more project documentation on Docker, some troubleshooting, and some basic commands, see:
[doc/docker.md](https://github.com/codeforpdx/recordexpungPDX/blob/master/doc/docker.md)


## Installation, deprecated:

This is a deprecated setup that runs the backend tests, the flask dev server, and/or the npm dev server natively. With Docker set up correctly you shouldn't have to use this. The above is a newly added feature but it *should* be the easiest setup, so if you have any trouble at all please ping the slack channel.

1. **[Fork](https://help.github.com/articles/fork-a-repo/#fork-an-example-repository)**,
	and **[clone](https://help.github.com/articles/fork-a-repo/#step-2-create-a-local-clone-of-your-fork)** the repo.

2. Install Python:

    * **Mac**

      To install the latest version of Python on Mac run:

          $ brew install python3

      <!-- -->
		note: This will pull the latest version of Python, so when Python 3.8 or
		greater is released it will install that version.

    * **Linux**

        - Ubuntu 18.04

			To install Python 3.7 on Ubuntu 18.04 run the command:
			```
			$ sudo apt-get install python3.7 -y
			```

        - Ubuntu 16.04

			To install Python 3.7 on Ubuntu 16.04 follow the instructions
			[here](https://github.com/codeforpdx/recordexpungPDX/wiki/Installing-python3.7-on-ubuntu-16.04).

    * **Windows**

      Developing this project on Windows is no longer supported in our documentation. The current approach some individual devs are using is to run linux in a VM. Anyone who wants to wrangle Windows is totally free to jump off the deep end! And then report back with supporting documentation :)

3. Install Pipenv

	Install the [pipenv](https://pipenv.readthedocs.io/en/latest/install)
	package manager which also automatically creates and manages virtual
	environments.

4. Install additional libraries needed for running the backend natively or with pipenv:

    * **Mac**

      ```
      brew install postgresql
      ```
      Note: this step is only required to meet a dependency for python's psycopg2 package, namely `libpq-dev`. The dev environment doesn't require a local installation of the database, because the database runs within the docker stack.

      It may be necessary to then run
      ```
      export LDFLAGS="-L/usr/local/opt/openssl/lib"
      ```
      More information on a Mac installation here: https://wiki.postgresql.org/wiki/Homebrew
    * **Linux**
      ```
      sudo apt-get install libpq-dev -y
      ```

5. Install NPM if you don't already have it installed. [This link provides
	instructions on how to install Node.js and NPM](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)

6. Install backend dependencies:

	A [Makefile](https://www.gnu.org/software/make/) controls installing
  python dependencies, removing build artifacts, and building / running the Docker stack locally.
	While in the directory of your local `recordexpungePDX` repo, install the
  backend dependencies by running:

	```
	$ make install
	```

  This will read `Pipfile` and install listed Python packages into a `Pipenv`
  virtualenv.

  Note: due to our new setup with docker, the `Pipfile` and `Pipfile.lock` files are no longer in the project root directory. Copy them if you want to use pipenv. More cleanup and removal of this deprecated setup is forthcoming.

7. Install frontend dependencies

	While in the directory of your local `recordexpungePDX` repo, enter into your
  command line and run:

  ```
	$ cd src/frontend

	$ npm install
  ```

8. Install docker

   * **Mac**

        - Follow installation instructions in:[Getting Started -- Docker on Mac OS X](https://medium.com/allenhwkim/getting-started-docker-on-mac-os-x-72c64670464a)

          (click on Get Docker for Mac [Stable])

   * **Linux**

        - First, follow: [Docker Installation](https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-using-the-repository)

        - Configure your user to run docker without sudo: https://docs.docker.com/install/linux/linux-postinstall/

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


which opens a bash shell inside the respective container. In the backend container, you can then run the python interactive shell `python3` or `pytest` commands.

To run a subset of test cases without first shelling into the docker container, you can use a docker `exec` command, which specifies a container by name and a runnable command in the container in a single step, e.g.: 

```
docker exec -t expungeservice pytest ./tests/[subdir]
```

To specify and run a subset of the test cases.

## Project Layout

`.flaskenv`: Environment variables read by `flask` command-line interface via [python-dotenv](https://github.com/theskumar/python-dotenv)

`Makefile`: GNU Makefile controlling installing dependencies and running the application

`Pipfile`: `Pipenv` file listing project dependencies

`config`: Project configuration files

`doc`: Developer-generated documentation

`settings.py`: `python-dotenv` configuration file

`src`: Source dir

`src/backend/expungeservice/app.py`: Flask application

## <a name="contributing"></a>Contributing

 1. **[Fork](https://help.github.com/articles/fork-a-repo/#fork-an-example-repository)** the repo on GitHub
 2. **[Clone](https://help.github.com/articles/fork-a-repo/#step-2-create-a-local-clone-of-your-fork)** the project to your own machine. Replacing YOUR-USERNAME with your github username.
   ```bash
    $ git clone https://github.com/YOUR-USERNAME/recordexpungPDX.git
   ```
 3. cd into recordexpungPDX
   ```bash
    $ cd recordexpungPDX
   ```
 4. Configure upstream to sync with your fork
   ```bash
    $ git remote add upstream https://github.com/codeforpdx/recordexpungPDX.git
   ```
 5. Create a branch to work on. Replacing BRANCH_NAME with a descriptive name of the work planned such as `update_contributing_doc`
   ```bash
     $ git checkout -b BRANCH_NAME
   ```
 6. **Commit** changes to your branch (never to master)
 7. **Push** your work back up to your fork
   ```bash
     $ git push
   ```
   - NOTE: The first time you do `git push` on your branch it will error with:
   ```bash
    fatal: The current branch BRANCH_NAME has no upstream branch.
    To push the current branch and set the remote as upstream, use

        git push --set-upstream origin BRANCH_NAME
   ```
   - Copy the output and run it. Then afterwords simply push more commits by running `git push`.
 8. Submit a **Pull request**

- NOTE: For future contributions be sure to sync master with upstream
```bash
  $ git checkout master
  $ git pull upstream master
  $ git checkout -b BRANCH_NAME
```

  Python code should follow the [PEP8 standard](https://www.python.org/dev/peps/pep-0008/). Notably:

  * **module** names should be lowercase and run together, e.g. `mymodule`
  * **class** names should be camel case, e.g. `MyClass`
  * **method** and variable names should be snake case, e.g. `my_method()` and `my_var`

## License

TODO: Add license
