
This tool runs the frontend and backend dev servers behind a shared nginx server, allowing both to pick up and publish local code changes right away. This setup bypasses a [CORS error](https://developer.mozilla.org/en-US/docs/Glossary/CORS) (Cross-Origin Resource Sharing) that would throw if the servers simply run natively at different ports.

The backend functions that hit the postgres database still need the docker stack running to host it, so this runs a docker stack setup containing only the the database.

The script ./launch_workspace.sh launches the four required processes but first performs a few commands to kill previously running flask and npm processes, and the app's regular docker stack since it would occupy the same ports.

Before running the script you'll need to have built the docker image for the new nginx server:

`docker build -t workspaceserver ./ -f Dockerfile.dev`

To stop the nginx server container, run:

`docker stop workspaceserver`

The custom docker stack that runs only a database will occupy the same port as the database container from our regular dev stack. So you'll want to take one down whenever starting the other. The manual docker command is:

`docker stack rm recexp_workspace_stack `

or

`docker stack rm recordexpungpdx `
