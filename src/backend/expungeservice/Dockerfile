FROM library/ubuntu
RUN apt-get update &&\
    apt-get install -y python3.7 python3.7-dev python3-pip curl &&\
    python3.7 -m pip install pip --upgrade &&\
    python3.7 -m pip install wheel

RUN mkdir -p /var/www/expungeservice
COPY . /var/www/expungeservice
WORKDIR /var/www/expungeservice
RUN python3.7 -m pip install -r requirements.txt && rm requirements.txt &&\
    python3.7 -m setup install 

# This exposes a port; docker-compose file sets mapping.
EXPOSE 5000

WORKDIR /var/www
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV FLASK_APP="expungeservice:create_app('development')"
ENTRYPOINT ["flask"]
CMD ["run", "--host=0.0.0.0", "--port=5000"]
