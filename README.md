# recordexpungPDX
A project to automate expunging qualifying criminal records.  This project is done in conjunction with the Multnomah County Public Defender's Office.


## Installation

Fork, and clone the repo.


### Install Pipenv

- Install the [pipenv](https://pipenv.readthedocs.io/en/latest/install) package manager which also automatically creates and manages virtual environments.

A [Makefile](https://www.gnu.org/software/make/) controls installing dependencies, running the Flask app, and removing build artifacts:

- Install dependencies:

Running:

```
$ make install
```

will read `Pipfile` and install listed Python packages into a `Pipenv` virtualenv.

- Run Flask app (also installs dependencies):

Running:

```
$ make run
```

will run the `Flask` app inside a `Pipenv` virtualenv.

- Clean:

Running:

```
$ make clean
```

will remove build artifacts.


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

 1. **Fork** the repo on GitHub
 2. **Clone** the project to your own machine
 3. **Commit** changes to your own branch
 4. **Push** your work back up to your fork
 5. Submit a **Pull request**

NOTE: Be sure to merge the latest from "upstream" before making a pull request!

## License

TODO: Add license
