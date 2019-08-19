
##Deployment

This directory and document contain information and make targets needed for deployment to our prod platform, Heroku.

Web deployment is broken into three parts, corresponding to the three services in our app stack:

 - the nginx server, which serves the frontend web files and proxies backend api requests, and publishes at the heroku url recordexpungpdx.herokuapp.com

 - the backend flask/wsgi app, which servces api requests that are called by the frontend app, and publishes at the heroku url recordexpungpdxapi.herokuapp.com

 - the database, which is deployed as a heroku postgres addon attached to the backend app.

The heruko app frontend and backend are each deployed as a Docker image which gets built locally and then pushed to the Heroku image registry. This process is quite handsoff and requires only the execution of a few Heroku commandline instructions.

We have Make targets (in the adjacent Makefile) for rebuilding and deploying the frontend and backend. Since these webapps don't store persistent data, we it's ok to just replace the existing images on Heroku with a new build.

Updating the database deployment needs accompanying data backup and restore ops. Database operations:

 - To run a sql script in the app's attached database:

 ```heroku pg:psql --app=recordexpungpdxapi -f ./path/to/scripts/script.sql ```

 -
####Additional dev notes

In order to make changes to the published apps, the user must be logged into the apps' owner account with `heroku login`

The frontend and backend apps each need to be "created" only once on Heroku, enabling push and deployment, using the following command:

 heroku apps:create recordexpungpdx
