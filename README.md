# recordexpungPDX
A project to automate expunging qualifying criminal records.  This project is done in conjunction with the Multnomah County Public Defender's Office. [Learn more in the wiki](https://github.com/codeforpdx/recordexpungPDX/wiki).

This README is covers project installation and getting started as a contributor. For more info:

Project design documentation: [doc/design.md](https://github.com/codeforpdx/recordexpungPDX/blob/master/doc/design.md)

Additional frontend documentation: [src/frontend/README.md](https://github.com/codeforpdx/recordexpungPDX/blob/master/src/frontend/README.md).

[![Build Status](https://travis-ci.com/codeforpdx/recordexpungPDX.svg?branch=master)](https://travis-ci.com/codeforpdx/recordexpungPDX)

## Table of Contents

- [Installation](#installation)
- [Running Components](#running-the-docker-stack)
- [Testing](#testing)
- [Project Layout](#project-layout)
- [Contributing](#contributing)
- [License](#license)

## Installation

Our dev environment uses pipenv for maintaining backend dependencies, and npm to develop the frontend. We use pipenv and pytest to develop backend code. Docker is used to build and deploy the app stack. A postgres database runs as a service within the docker stack, which exposes a connection locally for running the test code in pipenv.

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

9. Create a local .env file

While in the directory of your local repo, run:
```
cp .env.example .env

```

##### Cleaning

While in the directory of your local repo, run:

```
$ make clean
```
in order to remove build artifacts.

## Running the Docker stack

Docker provides a fully sandboxed virtual environment from which we will run the app in production. The project stack must be built and run locally for the complete set of tests (discussed below) to pass, because it runs a local instance of the database. While in the directory of your local repo, run:

```
docker swarm init
```

This enables docker to run a stack locally and only needs to be run once.

```
make dev
```

This command builds the docker images (web server, flask backend, and postgres database) and launches a docker stack running the three services. Verify the backend is serving requests by navigating to `http://localhost:5000/api/hello`. The frontend can be reached at `http://localhost:3000`.

Note: running docker requires root access by default. If you try to run this command with sudo it may fail because it messes up pipenv. Be sure to configure docker so you can run it without using sudo (see above).

Once you start making local code changes, you'll want to familiarize with some essential Docker commands. For more project documentation on our Docker setup, troubleshooting, and some basic commands, see:
[doc/docker.md](https://github.com/codeforpdx/recordexpungPDX/blob/master/doc/docker.md)


## Testing

Currently using [pytest](https://docs.pytest.org) for testing.
Run all tests with the following command:

```bash
$ make test
```

All of these tests should pass if you have correctly set up the backend dev environment.


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
