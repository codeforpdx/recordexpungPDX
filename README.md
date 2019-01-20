# recordexpungPDX
A project to automate expunging qualifying criminal records.  This project is done in conjunction with the Multnomah County Public Defender's Office.

[![Waffle.io - Columns and their card count](https://badge.waffle.io/CodeForPortland/recordexpungPDX.svg?columns=all)](https://waffle.io/CodeForPortland/recordexpungPDX)

[![Build Status](https://travis-ci.com/CodeForPortland/recordexpungPDX.svg?branch=master)](https://travis-ci.com/CodeForPortland/recordexpungPDX)
## Installation

Fork, and clone the repo.

to install python3.7 on mac run:
```
brew install python3
```

to install python3.7 on ubuntu 18.04 just run the command:
```
sudo apt-get install python3.7 -y 
```

to install python3.7 on ubuntu 16.04 follow the instructions [here](https://github.com/CodeForPortland/recordexpungPDX/wiki/Installing-python3.7-on-ubuntu-16.04)



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

### Testing

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
    $ git remote add upstream https://github.com/CodeForPortland/recordexpungPDX.git
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
