FROM node:latest as build
RUN mkdir /usr/src/app
ENV PATH /usr/src/app/node_modules/.bin:$PATH
COPY package.json /usr/src/app/package.json

WORKDIR /usr/src/app
RUN npm install
COPY . /usr/src/app

# For some reason, the HOST environment variable is only applied when addeed to
# a .env file. Adding the variable in docker-compose didn't take. Since .env files
# are gitignored in this project, we save the variable in websrver.env and map it
# to the correctly named file in the container.
COPY webserver.env /usr/src/app/.env
CMD ["npm", "start"]