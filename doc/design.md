RecordSponge System
=====================

Some thoughts on the RecordSponge System.


Table of Contents
-----------------
- [Project Stack](#project-stack)
- [Project Layout](#project-layout)
- [User Flow](#user-flow)
- [Frontend Routes](#frontend-routes)
- [Backend Endpoints](#backend-endpoints)

Project Stack
-------------

The development app stack is deployed as three services in a Docker Compose network:

[ expungeservice ] -- Python 3.7, Flask

[ node ] -- NodeJS, React


Project Layout
--------------

This is a high-level [tree](https://linux.die.net/man/1/tree) of the project only listing "notable" folders/files.
```
.
├── Makefile : GNU Makefile with targets for working with local dev environment
├── config : Project configuration files
│   └── postgres
├── doc : Developer-generated documentation folder
├── docker-compose.yml : Docker Compose file that `make` targets invoke
└── src : Source directory
    ├── backend
    │   ├── Dockerfile
    │   ├── Pipfile : Pipenv file listing backend project dependencies
    │   ├── Pipfile.lock
    │   ├── expungeservice
    │   │   └── app.py : Flask application start
    │   ├── mypy.ini : Configuration file to the mypy type checker 
    │   ├── setup.py
    │   └── tests
    ├── frontend
    └── ops
        ├── Makefile : GNU Makefile with targets for building & deploying staging/prod images
        └── docker/expungeservice
            └── Dockerfile
```

User Flow
---------

User is directed to landing page

User has option to search or view manual

If user chooses search:

- User is direct to log into remote site (OECI)

- User enters search terms

- Service logs into remote site (OECI)

- Service does search on remote site (OECI)

- Remote site (OECI) returns HTML page of results

- Service scrapes results

- Service parses scraped results

- Service makes decision based on Expunger rules

- User is directed to page of pretty-fied results

- User has option to search again or go back to landing page




Frontend Routes
---------------

These routes are set up in the front-end application for navigating between the different views.

`/`

Main page

- Search: search remote system
- Manual


`/search`

Search page

- Form for entering first name, last name, dob
- Shows results of search

Backend Endpoints
-----------------

These endpoints comprise our API. All requests of these endpoints go through the web server.

**`POST`** `/api/oeci_login/`

Attempts to log into the OECI web portal with the provided username and password. If successful, closes the session with OECI and returns those credientials encrypted in a cookie. No "logged in" state is maintained with the remote site. Instead, subsequent calls to the /api/search endpoint use the encrypted credentials to log in again before performing the search. Credentials are encrypted with Fernet cipher using the app's `JWT_SECRET_KEY` attribute as the symmetric key.


Required headers:

- `Authorization: <JWT string>`

`POST` body:

- format: `JSON`
- fields:
    * oeci_username
    * oeci_password

Returns: encrypted cookie

- response body empty
- cookie: encrypted json string
  - fields:
    * oeci_username
    * oeci_password


Status codes:

- `201 CREATED`: credentials valided, encrypted, and returned
- `400 BAD FORMAT`: missing data in request body or one or more fields
- `401 UNAUTHORIZED`: authorization rejected; missing or invalid auth token
- `401 UNAUTHORIZED`: oeci authorization rejected; incorrect username or password


**`POST`** `/api/search`

Performs search of remote system, using the search params provided in the request body. The oeci_login
endpoint must get called beforehand to obtain the oeci_token cookie.

Returns a serialized version of the Record object in the json response body. The `record` data object matches the format specified in /doc/results_format.json

Also records anonymized stats based on the rearch results.

Required headers:

- `Authorization: <JWT auth_token>`

Required cookie:

- `{oeci_token: <encrypted result of /api/oeci_login attempt>}`

`POST` body:

- format: `JSON`
- fields:
    * TODO: Fill in

Returns: Search results

- format: `JSON`
- fields:
    * TODO: Fill in


Data Model
----------

TODO: Dynamically generate this section based on dataclasses in [models](../src/backend/expungeservice/models/)
