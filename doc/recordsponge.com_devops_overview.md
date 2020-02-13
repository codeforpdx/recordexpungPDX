## Notes about https://recordsponge.com/

Our domain https://recordsponge.com/ is registered through [Namecheap](https://www.namecheap.com/) and has its nameservers pointed at [DigitalOcean](https://www.digitalocean.com/) where we host the application.

We have a single [Nginx](https://www.nginx.com/) file at `/etc/nginx/sites-available/recordexpunge-nginx.conf` that proxies frontend requests to `/usr/share/nginx/html` where the statically packaged [React](https://reactjs.org/) app files exist and backend requests to `localhost:3031` where we serve our [Flask](https://flask.palletsprojects.com) app through [uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/).

Through [Psycopg](https://www.psycopg.org/), the backend communicates with the [psql](https://www.postgresql.org/) DB and stores authentication details and anonymized statistics in a database `record_sponge_db`.

We use [LetsEncrypt](https://letsencrypt.org/) for our SSL certificate. We have them set to autorenew as follows:

```
$ sudo crontab -e
# m h  dom mon dow   command
0 5 * * 1 sudo certbot renew
0 5 * * 1 sudo service nginx restart
```

We have enabled 4GB of swap.

```
$ sudo mkswap /swap
Setting up swapspace version 1, size = 3.9 GiB (4145737728 bytes)
no label, UUID=31f4b6de-d752-4b83-ba6a-2f27fb94784e
```

No [Docker](https://www.docker.com/) containers have been used so far on production but that may change as the deployment pipeline is WIP.