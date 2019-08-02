
Features:

(notes related to first nginx PR, some features and readme notes subject to change )
* Docker image that contains the static web content and the configured nginx server process, which handles uri redirection for api calls.
* Stanza in docker-compose.yml defining the webserver service.
* port 3000 of the webserver container is published to 3000 in docker-compose.dev.yml, matching the behavior of running the frontend with node. I assume in prod the server would instead publish to 80 or 443, which are already exposed by the nginx base image.
* New make target called webserver_image that builds the docker image. This executes the frontend build process before writing the result into the docker image.
* In the make file, webserver_image is added to the dev target which builds the complete docker stack.
* The Nginx base docker image already redirects the server access and error logs to std_out and std_err, which get captured by docker logging.
* The expungeservice Docker image now runs a wsgi server instead of the Flask server. The Nginx reverse-proxy is configured to forward api calls in wsgi instead of http.
* The nginx server will need to be configured for https when we have a certificate. For that we need a domain name. For now I think it's fine to merge this branch to Master without it since we're still a ways from deployment to prod.
* Some of this will be refactored as part of #174 but that is out of scope for this PR.
* The nginx config file specifies the server name, which is distinct for dev vs prod. I’m not sure where is the best point in the workflow to make the distinction between which of these nginx configurations is copied into the Docker image. E.g. no other containers have different Dockerfiles for dev vs prod. Should the make target instead copy the correct nginx config file locally before building the image?
* All the expungeservice endpoints have a leading "/api/" in their uri. I added this to the /hello/ endpoint also for consistency (I think keeping this endpoint for now makes sense because it's the only one that doesn't require any data in the request).
* The nginx Dockerfile is based on the tutorial here: https://medium.com/thepeaklab/how-to-deploy-a-react-application-to-production-with-docker-multi-stage-builds-4da347f2d681
* Building the new docker image in Travis slows down the build again :((((
