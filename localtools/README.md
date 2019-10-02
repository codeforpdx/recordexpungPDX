
### Workspace Nginx Server

This tool is depracated and will be deleted soon. Its purpose is subsumed by our main install setup using docker-compose.

This runs the frontend and backend dev servers behind a shared nginx server, allowing both to pick up and publish local code changes right away. This setup bypasses a [CORS error](https://developer.mozilla.org/en-US/docs/Glossary/CORS) (Cross-Origin Resource Sharing) that would throw if the servers simply run natively at different ports.

The backend functions that hit the postgres database still need the docker stack running to host it, so this runs a docker stack setup containing only the the database.

The script ./launch_workspace.sh launches the four required processes but first performs a few commands to kill previously running flask and npm processes, and the app's regular docker stack since it would occupy the same ports.

The new proxy server runs at socket 3005! Navigate to that in the browser even though npm launches the browser for 3000. If you load socket 3000 in the browser the redirect probably won't work correctly.


### EXTRA REQUIRED STEPS:

 - Before running the script you'll need to have built the docker image for the new nginx server:

`docker build -t workspaceserver ./ -f Dockerfile.dev`


 - The custom docker stack that runs only a database container will occupy the same port as the database container from our regular dev stack. So you'll want to take one down whenever starting the other. The manual docker commands (to remove the workspace DB or Dev DB) are:

`docker stack rm recexp_workspace_stack `

or

`docker stack rm recordexpungpdx `

 - That only removes the PSQL container that supports the actual database content. the data is stored in a Docker volume, which persists separately. So if the database ever changes, i.e. when we do a tables refactor, you will need to drop the old database attached to THIS stack, just like we do for the regular Dev stack (and first destroy the docker container that is attached to the volume).

```
docker rm -f recexp_workspace_stack
docker volume rm recexp_workspace_stack_database_storage

```

 - To stop the nginx server container, run:

`docker stop workspaceserver`

 - The npm and flask dev servers run in detached mode, so kill them with:

` killall flask node`
