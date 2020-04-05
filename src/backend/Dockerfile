FROM python:3.7-alpine AS base
LABEL authors="Kenichi Nakamura <kenichi.nakamura@gmail.com>"

RUN pip install pipenv
RUN apk update

RUN mkdir -p /var/opt/backend/expungeservice
WORKDIR /var/opt/backend

ENV WORKON_HOME=/var/opt/venvs
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN apk add libffi openssl libpq

# ---

FROM base AS build

RUN apk add build-base git libffi-dev openssl-dev postgresql-dev

COPY Pipfile* setup.py /var/opt/backend/
RUN cd /var/opt/backend && pipenv install

# ---

FROM base

COPY --from=build /var/opt/venvs /var/opt/venvs

EXPOSE 5000
CMD ["pipenv", "run", "uwsgi", "--py-autoreload", "1", "--http", "0.0.0.0:5000", "--module", "expungeservice.wsgi", "--die-on-term", "--uid", "nobody"]
