FROM python:3.7-alpine AS build
LABEL authors="Kenichi Nakamura <kenichi.nakamura@gmail.com>"

RUN pip install pipenv
RUN apk update
RUN apk add build-base libffi-dev openssl-dev postgresql-dev

RUN mkdir -p /var/opt/backend/expungeservice
COPY Pipfile* setup.py /var/opt/backend/
ENV WORKON_HOME=/var/opt/venvs
RUN cd /var/opt/backend && pipenv install

# ---

FROM python:3.7-alpine
LABEL authors="Kenichi Nakamura <kenichi.nakamura@gmail.com>"

RUN pip install pipenv
RUN apk update
RUN apk add libffi openssl libpq
ENV WORKON_HOME=/var/opt/venvs
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

COPY --from=build /var/opt/venvs /var/opt/venvs

WORKDIR /var/opt/backend
EXPOSE 5000
CMD ["pipenv", "run", "uwsgi", "--py-autoreload", "1", "--http", "0.0.0.0:5000", "--module", "expungeservice.wsgi", "--die-on-term"]
