The deployment to prod requires some config files and run commands distinct from dev deployment

Web deployment is broken into three parts, corresponding to the three services in our app stack:

 - the nginx server, which serves the frontend web files and proxies backend api requests, and publishes at the heroku url recordexpungpdx.herokuapp.com
 - the backend flask/wsgi app, which servces api requests that are called by the frontend app, and publishes at the
heroku url recordexpungpdxapi.herokuapp.com
 - the database, which is deployed as a heroku postgres addon attached to the backend app.

The heruko app is deployed as a Docker image which gets built locally and then pushed to the Heroku image registry. This process is quite hands-off and requires only the execution of two Heroku command-line instructions.

We have Make targets for rebuilding and deploying the frontend and backend. Since the apps don't store persistent data, we can just replace the existing images on Heroku with a new build.


The Makefile in the deployment/ directory contains commands for building and pushing the frontend and backend images.
