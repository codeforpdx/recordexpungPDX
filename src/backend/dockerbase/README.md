This is a docker image containing the more static content of the expungeservice docker image. This image is pushed onto the Docker Hub and intended to reduce the project build time. 

This image contains any dependencies other than project source code. Any changes to the Dockerfile should be pushed to the Docker Hub.

To rebuild and then push the image, use:

`docker build -t recordexpungpdx:expungeservicebase ./
docker push recordexpungpdx:expungeservicebase`

To push to the project hub you will need to have logged in with

`docker login`

using the project login credentials. 
