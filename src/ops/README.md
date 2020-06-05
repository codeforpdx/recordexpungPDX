RecordSponge Ops
================

Details on developer operations, deploy steps, configurations, etc.

## Goals

* make initial developer set up as simple as possible (`make new`)
* make staging, production, etc. deploys as simple as possible (`cd src/ops && make staging`)
* keep dev, staging, and production environments as similar as possible
* make developing either frontend or backend features as simple as possible
    * support HMR dev server for frontend dev, or static files for backend-only
    * bind mount local source tree into dev containers
    * support test/style watchers/linters

## DevOps

This section describes the configuration of the "local" developer enviroment
with notes addressing specific decisions made to support the overall goals of
this initiative.

### Implementation

The local developer environment for this project relies on 3 containers:

* Node to run react-scripts, handle HMR dev server
* Python 3.7 to serve the Flask app (API & static files)

We only customize the Python container and use published base images for Node
and Postgres directly. The Python container is configured to have all the
run-time dependencies and the virutalenv defined by `Pipfile.lock`.

For node, there are no run-time requirements, since react-scripts will build a
complete static tree of HTML, CSS, and JavaScript for production deploys. The
Flask app is configured to serve these statically built files. This keeps
deploys simple, see [below](#Deploys).

#### Python dependencies

When Python dependencies change, an owner of the
[RecordSponge](https://hub.docker.com/u/recordsponge) Docker Hub ID needs to
build and push a new image. This does not prevent a developer from testing with
different dependencies, but pushing the dev image is considered an official step
and provides the rest of the group with the new pre-built image.

Testing new dependency locally:

```
$ vim src/backend/Pipfile
$ make backend_build backend_reload backend_logs
```

Pushing new `expungeservice:dev` image:

```
$ docker login
$ make push
```

_Dependency changes should be thoroughly vetted before both being merged in and
pushing a new dev image._

NOTE: virtualenv is stored *inside the image* at `/src/venvs`

#### Node dependencies

The Node container is configured to use `npm install && npm run start` as its
run command. This will attempt to intall node modules each time the container
is started, then fire up the HMR dev server.

Changing node module dependencies:

```
$ vim src/frontend/package.json
$ docker-compose restart node

```

NOTE: `node_modules` is a named volume, mounted into the node container at the
path `/src/frontend/node_modules`. This keeps the node\_modules tree off of the
local filesystem, and preserves it across container lifecycles.

##

## Deploys

### Image tags

We use the `:dev` image tag to denote an python:3.7-alpine based image that has
all the run-time dependencies but no source. It expects source trees to be
bind-mounted into a container running this image.

Conversely, we use the `:staging` (and soon `:prod`) tags to denote images that
are based on `:dev` but have full backend source & frontend build artifacts
copied into the image. These images are fully-contained, and deployable on
any platform, using only ENV variables to configure TIER.

### hub.docker.com ID and config

A `recordsponge` organization has been created on Docker hub. The `expungeservice`
repository under this org contains images with tags for `dev` (local), `staging`
(dev.recordsponge.com), and `prod` (recordsponge.com).

### DigitalOcean host config

An Ubuntu 18.04 host has been stood up to serve `*.recordsponge.com`. This host
has PostgreSQL 10, nginx, and Docker installed.

#### SSH config

To connect to this host, supply your SSH *public* key to someone with access.
Add the following to your `~/.ssh/config` file:

```
Host recordsponge
    User username
    Hostname recordsponge.com
    IdentityFile ~/.ssh/codeforpdx_ed25519
```

Replace `username` with yours, and `codeforpdx_ed25519` with your SSH *private*
key. You should now be able to connect with:

```
$ ssh recordsponge
```

#### TLS/SSL config

LetsEncrypt is fully configured. See:

* `/etc/nginx/sites-available/recordexpunge-nginx.conf`.
* `/etc/nginx/sites-available/dev.recordsponge.com.conf`.
* `/etc/cron.d/certbot`
* `/var/spool/cron/crontabs/root`

#### nginx config

* `proxy_pass` proxy method
* terminates SSL, passes everything else to port
* single-container listening on port

| domain | conf file |
|-|-|
| recordpsonge.com | `/etc/nginx/sites-available/recordexpunge-nginx.conf` |
| dev.recordpsonge.com | `/etc/nginx/sites-available/dev.recordsponge.com.conf` |
|-|-|

### DNS config

TODO: find out details

### Steps to deploy

NOTE: These steps assume the above configurations and a tangible example exists in
the `staging` and `prod` targets of [src/ops/Makefile](/src/ops/Makefile).

1. build, tag, and push new image
2. connect to production host
3. pull new image
4. stop container
5. start container from new image

See [staging.yml](../../.github/workflows/staging.yml) to see how Github automatically deploys a new build after each PR to staging.
