Project Development Tips
========================

A few things to do when developing the frontend or backend.

## When Pulling Changes From Master

These instructions are outdated given our current docker dev setup.

Code changes to the database (tables or functions) are not reflected in the Docker stack until you manually rebuild the database Docker image and replace the database Docker Volume, which is a persistent storage container attached to the ephemeral Docker stack container.
 
 To perform both of these steps:
 
 ```
 make dev_down
 make dev_drop_database
 make dev_build
 make dev_up
 
 ```
 
If you don't want to lose the contents of your database ... well we don't currently have a tool to automatically export/import the data. But we need it! See Issue #299, and feel free to add this feature.


## Create a Local User

These instructions are outdated given our current docker dev setup.

You can create user accounts manually in the database if you want to. Here's how:

1. Choose a password and compute its bcrypt hash:

In the project directory, run
```
docker exec -ti pipenv run python
```
to open the python interactive terminal with the project's dependencies loaded. Then run

```
$ from werkzeug.security import generate_password_hash
$ generate_password_hash('your_password')
```

2. Choose an email address and insert it and your password hash into the database:

In the project directory, run
```
make dev_psql
```

This launches the PSQL interactive environment in the project's postgres docker container. In this terminal, run:

```
$ SELECT * FROM USERS_CREATE('your_email', 'your_hashed_password', 'your name', 'your group name', true);
```

providing your actual email and hashed password each in the single-quotes.

This runs a custom SQL function which inserts your user credentials.


## Test Backend API calls

See design.md for the specifications of each API endpoint.

To test the endpoint calls for /auth_token and /users respectively, run:

```
$ curl -X GET -i -H "Content-Type: application/json" "localhost:5000/api/auth_token" --data '{"email":"your_email", "password":"your_password"}'
```

which should return something like this:

```
{
  "auth_token": "[long hash string]"
}
```

the auth_token string provides a claim that a particular user is logged in. Subsequent endpoints that require authorization will read the auth_token string to verify the logged-in user's credentials.

To run the /users/ POST endpoint, run

```
$ curl -X POST -i -H "Content-Type: application/json" -H "Authorization: Bearer [auth-string]" localhost:5000/api/users --data '{"email":"new_email", "password":"new_password", "admin":false}'
```

replacing `[auth-string]` with the auth_token value you just received. This should return:

{
  "admin": false,
  "email": "new_email",
  "timestamp": "[timestamp]"
}
