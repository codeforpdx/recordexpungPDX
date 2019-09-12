# A combined setup for running the frontend and backend dev servers natively
# so that they reflect local code changes right away.
# This setup still runs the database from the docker stack
# And an nginx server as a separate docker service to manage app requests and avoid CORS issues

# BEFORE LAUNCH: you need to build the workspaceserver Docker image.
# in the /localtools/workspace/ directory, run:
# docker build -t workspaceserver ./ -f Dockerfile.dev
#

# launch the nginx server that redirects to the frontend and backend dev servers
docker rm -f workspaceserver
echo "deleting the previous workspace server"

sleep 3
docker run --name workspaceserver --network "host" -p 3005:3005 -d workspaceserver
echo "workspace nginx server launched"

#take down the local docker stack because it occupies the same frontend and backend ports
make -C ../ dev_stop
#- counter=0 ; while ((counter < 20)) &&  pg_isready --host=localhost --port=5432 --dbname=$PGDATABASE ; do sleep 3; let counter=counter+1; done
echo "halting the dev stack"
sleep 3

kill $(pgrep -f node)
echo "halting other node processes"

kill $(pgrep -f flask)
echo "halting other flask processes"
sleep 3



#launch a limited configuration of the dev docker stack which only runs the database
docker stack deploy -c docker-compose.workspace.yml recexp_workspace_stack
echo "launched a docker stack with db only"


#start the flask and npm servers.
npm --prefix ../src/frontend/ start >> /dev/null &
echo "launched the npm dev server"

export FLASK_ENV=development

cd ../ && pipenv run flask run  &
echo "launched the flask dev server"

# For some weird reason the setup has sometimes worked if you then take down the nginx
# server. The frontend dev server's calls still get routed to the backend. I have no idea why.
# so this command  does that, comment if you want to:

## docker stop workspaceserver
