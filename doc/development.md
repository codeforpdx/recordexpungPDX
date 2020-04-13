Project Development Tips
========================

This document describes a few things that may be useful for development.

## Database named volume

The postgres database service uses a named Docker volume `recordexpungpdx_postgresql_data` that persists across container lifecycles. To remove this and other volumes created by the compose file, use `make clobber`.

## In-project guide to using Docker:

Available here: [doc/docker.md](docker.md)

## Create a Local User

You can create user accounts manually in your local database if you'd like to do so for any manual testing. Here's how:

1. Choose a password and compute its bcrypt hash:

In the project directory, run:

```
$ docker-compose exec expungeservice pipenv run python
```

to open the python interactive terminal with the project's dependencies loaded. Then run:

```python
>>> from werkzeug.security import generate_password_hash
>>> generate_password_hash('your_password')
```

2. Choose an email address and insert it and your password hash into the database:

In the project directory, run:

```
$ docker-compose exec --user=postgres postgres psql record_expunge_dev
```

This launches the PSQL interactive environment in the project's postgres docker container. In this terminal, run:

```sql
record_expunge_dev=# SELECT * FROM USERS_CREATE('your_email', 'your_hashed_password', 'your name', 'your group name', true);
```

providing your actual email and hashed password each in the single-quotes.

This runs a custom SQL function which inserts your user credentials.


## Manually Testing Backend API calls

See design.md for the specifications of each API endpoint.

To test the endpoint calls for /auth\_token and /users respectively, run:

```
$ curl -X GET -i -H "Content-Type: application/json" "localhost:5000/api/auth_token" --data '{"email":"your_email", "password":"your_password"}'
```

which should return something like this:

```json
{
  "auth_token": "[long hash string]"
}
```

the auth\_token string provides a claim that a particular user is logged in. Subsequent endpoints that require authorization will read the auth\_token string to verify the logged-in user's credentials.

To run the /users/ POST endpoint, run

```
$ curl -X POST -i -H "Content-Type: application/json" -H "Authorization: Bearer [auth-string]" localhost:5000/api/users --data '{"email":"new_email", "password":"new_password", "admin":false}'
```

replacing `[auth-string]` with the auth\_token value you just received. This should return:

```json
{
  "admin": false,
  "email": "new_email",
  "timestamp": "[timestamp]"
}
```

## Mock Endpoints that make 3rd-party requests:

We have an alternate Docker configuration that mocks the /api/search and /api/oeci endpoint behavior. See [src/frontend/developerUtils/developerUtils.md](../src/frontend/developerUtils/developerUtils.md)
