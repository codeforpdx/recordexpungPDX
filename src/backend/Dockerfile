FROM python:3.7-alpine AS base
LABEL authors="Kenichi Nakamura <kenichi.nakamura@gmail.com>"

RUN pip install pipenv
RUN apk update

RUN mkdir -p /src/backend/expungeservice
WORKDIR /src/backend

ENV WORKON_HOME=/src/venvs
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN apk add libffi openssl libpq

# ---

FROM base AS build

RUN apk add build-base git libffi-dev openssl-dev postgresql-dev

COPY Pipfile* setup.py /src/backend/
RUN cd /src/backend && pipenv install

# ---

FROM base

COPY --from=build /src/venvs /src/venvs

EXPOSE 5000
CMD ["pipenv", "run", "uwsgi", "--py-autoreload", "1", "--http", "0.0.0.0:5000", "--module", "expungeservice.wsgi", "--die-on-term", "--uid", "nobody"]
