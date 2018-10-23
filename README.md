# recordexpungPDX
A project to automate expunging qualifying criminal records.  This project is done in conjunction with the Multnomah County Public Defender's Office.

## Installation

Fork, and clone the repo.

### Install Pipenv

- Install the [pipenv](https://pipenv.readthedocs.io/en/latest/install) package manager which also automatically creates and manages virtual environments.

- Install dependencies
```
    $ pipenv install
```

- Create postgres db
```
    $ createdb recordexpung_pdx_db
```

## Usage

Run:
```
    $ pipenv run python run.py
```


## <a name="contributing"></a>Contributing

 1. **Fork** the repo on GitHub
 2. **Clone** the project to your own machine
 3. **Commit** changes to your own branch
 4. **Push** your work back up to your fork
 5. Submit a **Pull request**

NOTE: Be sure to merge the latest from "upstream" before making a pull request!

## License

TODO: Add license
