
## Features:
* Docker image that contains static content and an nginx config file which does the app uri redirect for the api.
* Stanza in docker-compose.yml defining the webserver service, and a link for the content directory to a new docker volume.
* port 3000 of webserver container published to 3000 in docker-compose.dev.yml. I assume in prod the server would instead publish to 80 or 443, which are already exposed by the nginx  base image.
* New make target called webserver_image that builds the docker image.
* In the make file, added the webserver_image target to the dev_deploy target’s dependencies.
* Missing feature: https configuration (and cert).
* The Nginx docker image already redirects the server access and error logs to std_out and std_err, so docker logging captures both. 
* The destination of static files in the image is just nginx's default directory for static files: /usr/share/nginx/html/ . 
* Building the image requires that the frontend code has already been built in src/frontend/build, as described in src/frontend/README.md (just cd to src/frontend and run "npm run build"). I don't know the best workflow to put these steps together so it's just manual for now.

## Behavior issue to be aware of:
* After visiting the webpage, nginx will forward requests to the backend only if you do a hard refresh (shift-F5) on the endpoint url. Otherwise, that url first hits a react service which redirects to the site’s login page instead of reaching the server (because react doesn't recognize the endpoint uri). This stackoverflow post describes the issue:
https://stackoverflow.com/questions/51120222/how-to-serve-react-app-and-django-blog-from-nginx

If this behavior doesn't impact the ability of frontend scripts to call those urls, then this redirect of urls in the browser's address bar doesn't matter. Either way it's a frontend issue, and the server is handling the backend urls just fine. 


## Design choices I’m uncertain about :
* the webserver make-target copies static build files into the nginx config folder; because that’s where the webserver image is being built, and Docker only sees the current directory and its subdirs during the image build. The make target then removes the copied files. Is there a nicer approach that fetches static web files from the correct build location?
* Nginx’s uri-forwarding to the backend server is expecting an http socket, and so currently works with the flask dev server. When we replace the flask server with uWSGI, an option would be to set its port protocol to uwsgi, and change the nginx to use uwsgi_pass instead of proxy_pass. But the uWSGI server can also be configured to accept http requests. I found that both configurations worked fine. 
* The nginx config file specifies the server name, which is distinct for dev vs prod. I’m not sure where is the best point in the workflow to make the distinction between which of these nginx configurations is copied into the Docker image. E.g. no other containers have different Dockerfiles for dev vs prod. Should the make target instead copy the correct nginx config file locally before building the image?
* Specifically, the only necessary difference I found between dev and prod configs is the server domain name. I didn't include a prod config file. 
* I'm not aware of other necessary nginx config values in the config files, though there isn't much besides the 2 location def blocks. 



