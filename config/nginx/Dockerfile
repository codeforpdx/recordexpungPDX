# Builds a webserver container that includes the web app static files

# Dockerfile based on the tutorial here:
#https://medium.com/thepeaklab/how-to-deploy-a-react-application-to-production-with-docker-multi-stage-builds-4da347f2d681

# with build instructions adjusted to match our project documentation

### STAGE 1: Static web files ###

FROM node as build
RUN mkdir /usr/src/app
ENV PATH /usr/src/app/node_modules/.bin:$PATH
COPY frontend/package.json /usr/src/app/package.json

WORKDIR /usr/src/app 
RUN npm install --silent
# RUN npm install react-scripts -g --silent # from tutorial but missing in project docs.
COPY ./frontend /usr/src/app
RUN npm run build

### STAGE 2: Webserver ###

FROM nginx

# FROM nginx:1.15.12-alpine 
# alpine is a skinny image (~5MB as opposed to >80MB for basic nginx)
# may be a useful replacement for optimization

COPY --from=build /usr/src/app/build /usr/share/nginx/html
RUN rm /etc/nginx/conf.d/default.conf 

COPY recordexpunge-nginx.dev.conf /etc/nginx/conf.d/

# EXPOSE 3000 # port is only exposed by running as a service within the docker stack 
