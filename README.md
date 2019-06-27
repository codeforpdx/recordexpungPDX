# recordexpungPDX
A project to automate expunging qualifying criminal records.  This project is done in conjunction with the Multnomah County Public Defender's Office. [Learn more in the wiki](https://github.com/codeforpdx/recordexpungPDX/wiki).

This README is primarily for the backend. For info on the frontend see [src/frontend/README.md](https://github.com/codeforpdx/recordexpungPDX/blob/master/src/frontend/README.md).

[![Build Status](https://travis-ci.com/codeforpdx/recordexpungPDX.svg?branch=master)](https://travis-ci.com/codeforpdx/recordexpungPDX)

## Table of Contents

- [Installation](#installation)
- [Running Components](#running-components)
- [Testing](#testing)
- [Project Layout](#project-layout)
- [Contributing](#contributing)
- [License](#license)

## Installation

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

      To install Python 3.7 on Windows, follow the instructions [in this guide.](https://wiki.python.org/moin/BeginnersGuide/Download).

3. Install Pipenv

	Install the [pipenv](https://pipenv.readthedocs.io/en/latest/install)
	package manager which also automatically creates and manages virtual
	environments.

4. Install additional libraries needed for running the backend natively or with pipenv:

    * **Mac**

      ```
      brew install postgresql
      ```
      It may be necessary to then run
      ```
      export LDFLAGS="-L/usr/local/opt/openssl/lib”
      ```
      More information on a Mac isntallation here: https://wiki.postgresql.org/wiki/Homebrew
    * **Linux**
      ```
      sudo apt-get install libpq-dev -y
      ```
    * **Windows**

      TBD

5. Install NPM if you don't already have it installed. [This link provides
	instructions on how to install Node.js and NPM](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)

6. Install backend dependencies:

	A [Makefile](https://www.gnu.org/software/make/) controls installing
  dependencies, running the Flask app, and removing build artifacts.
	While in the directory of your local `recordexpungePDX` repo, install the
  backend dependencies by running:

	```
	$ make install
	```

	Make will read `Pipfile` and install listed Python packages into a `Pipenv`
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

Follow installation instructions in:

    [Getting Started -- Docker on Mac OS X](https://medium.com/allenhwkim/getting-started-docker-on-mac-os-x-72c64670464a)

(click on `Get Docker for Mac [Stable])

    * **Linux**

[Ubuntu Installation](https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-using-the-repository)
Links to install instructions for other linux distros listed in the sidebar.

9. Create a local .env file

While in the directory of your local repo, run:
```
cp .env.example .env

```
## Running Components

### Backend

#### Running Backend Development Server

While in the directory of your local repo, run:

```
$ make run
```

Doing so runs the `Flask` app inside a `Pipenv` virtualenv (the `Flask` app will
also install dependencies as part of this process). On success, a
development server for the backend should be started on `http://localhost:5000`.
To check this, navigate to `http://localhost:5000/hello`. If everything worked
correctly, your browser should display the text `Hello, world!`.

##### Cleaning

While in the directory of your local repo, run:

```
$ make clean
```
in order to remove build artifacts.

#### Running the Docker stack

Docker provides a fully sandboxed virual environment from which we will run the app in production. The project stack must be built and run locally for the complete set of tests (discussed below) to pass, because it runs a local instance of the database. While in the directory of your local repo, run:

```
docker swarm init
make dev
```

For more project documentation on our Docker setup, troubleshooting, and usage basics, see:
https://github.com/codeforpdx/recordexpungPDX/blob/master/doc/docker.md

## Testing

Currently using [pytest](https://docs.pytest.org) for testing.
Run all tests with the following command:

```bash
$ make test
```

## Project Layout

`.flaskenv`: Environment variables read by `flask` command-line interface via [python-dotenv](https://github.com/theskumar/python-dotenv)

`Makefile`: GNU Makefile controlling installing dependencies and running the application

`Pipfile`: `Pipenv` file listing project dependencies

`config`: Project configuration files

`doc`: Developer-generated documentation

`settings.py`: `python-dotenv` configuration file

`src`: Source dir

`src/backend/expungeservice/app.py`: Flask application
`

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


## License

TODO: Add license
