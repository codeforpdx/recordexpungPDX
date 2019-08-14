Record Expunge Web Deployment
=============================

An overview

We serve our app using the free webapp hosting service Heroku deployed using Docker.
Our app is deployed as two Heroku apps each associated with its own URL, containing the frontend and backend portions of the app stack.



Deployment Commands:
---------
In the terminal, use `heroku` commands to build docker images locally and then push to the heroku image registry for deployment.

First, use the project login credentials to access heroku admin:
```
heroku login
```

The heroku projects for the frontend and backend need to be already created and associated with this login account.


```
heroku create recordexpungpdx
heroku create recordexpungpdxapi
```

### Frontend

While in the project/src/frontend subdir of the project directory, run:

```
heroku container:push --recursive --app=recordexpungpdx
heroku container:release web --app=recordexpungpdx
```

The `--recursive` option instructs Heroku to search the current directory for files named Dockerfile.\*. It locates the file Dockerfile.web, and builds this Docker image to deploy online as the web container serving our app.

To view app logs:

```
heroku logs --tail --app=recordexpungpdxapi
```

### Backend

While in the project/src/backend subdir of the project directory, run:
