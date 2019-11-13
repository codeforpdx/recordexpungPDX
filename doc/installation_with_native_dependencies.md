## Installation, deprecated:

This is a deprecated setup that runs the backend tests, the flask dev server, and/or the npm dev server natively.

1. Install Python:

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

2. Install Pipenv

	Install the [pipenv](https://pipenv.readthedocs.io/en/latest/install)
	package manager which also automatically creates and manages virtual
	environments.

4. Install an additional library needed for allowing the backend to connect to psql:

    * **Mac**

      ```
      brew install postgresql
      ```
      Note: this step is only required to meet a dependency for python's psycopg2 package, namely `libpq-dev`. The dev environment doesn't require a local installation of the database, because the database runs within the docker stack.

      It may be necessary to add the following to \~/.bashrc
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
