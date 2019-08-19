Record Expunge Web Deployment
=============================

This directory and document contain information and make targets needed for deployment to our prod platform, Heroku.

###An overview

We serve our app using the free webapp hosting service Heroku, deployed using Docker.
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

```
heroku container:push --recursive --app=recordexpungpdxapi
heroku container:release web --app=recordexpungpdxapi
```

Once these apps are pushed to heroku, they should be running at
https://recordexpungpdx.herokuapp.com and
https://recordexpungpdxapi.herokuapp.com respectively.


The database is deployed as a heroku postgres addon attached to the backend app.

### Design and Dev notes:


The heruko app frontend and backend are each deployed as a Docker image which gets built locally and then pushed to the Heroku image registry. This process is quite handsoff and requires only the execution of a few Heroku commandline instructions.

We have Make targets (in the adjacent Makefile) for rebuilding and deploying the frontend and backend. Since these webapps don't store persistent data, we it's ok to just replace the existing images on Heroku with a new build.

Updating the database deployment needs accompanying data backup and restore ops. Database operations:

 - To run a sql script in the app's attached database:

 ```
 heroku pg:psql --app=recordexpungpdxapi -f ./path/to/scripts/script.sql
 ```
