Project Development Tips
========================

A few things to do when developing the frontend or backend.

## Create a Local User

In order to call API endpoints locally, e.g. while working on the frontend, you will need login credentials already stored in the local database. These are needed to obtain a JWT auth token (required for most endpoints). To do so:

1. Choose a password and compute its bcrypt hash:

In the project directory, run
```pipenv run python
$ from werkzeug.security import generate_password_hash
$ generate_password_hash('your_password')
```

2. Choose an email address and insert it and your password hash into the database:

In the project directory, run
```
make dev_psql
=# SELECT * FROM CREATE_USER('your_email', 'your_hashed_password', true);
```

## Test Backend API calls

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

and then run

```
$ curl -X POST -i -H "Content-Type: application/json" -H "Authorization: Bearer [auth-string]" localhost:5000/api/users --data '{"email":"new_email", "password":"new_password", "admin":false}'
```

replacing `[auth-string]` with the auth_token value you just received. This should return:

{
  "admin": false,
  "email": "new_email",
  "timestamp": "[timestamp]"
}
