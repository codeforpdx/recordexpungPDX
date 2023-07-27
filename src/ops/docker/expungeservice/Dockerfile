FROM python:3.9 AS base
LABEL authors="Kenichi Nakamura <kenichi.nakamura@gmail.com>"

RUN pip install --upgrade pip && \
      pip install pipenv
RUN apt update

RUN mkdir -p /src/backend/expungeservice
WORKDIR /src/backend

ENV WORKON_HOME=/src/venvs
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN apt install -y wkhtmltopdf openssl

# ---

FROM base AS build

RUN apt install git libffi-dev

COPY Pipfile* setup.py /src/backend/
RUN cd /src/backend && pipenv install

COPY backend /src/backend
RUN mkdir -p /src/backend/logs && chown nobody /src/backend/logs
RUN mkdir -p /src/backend/flask_session && chown nobody /src/backend/flask_session

COPY frontend /src/frontend

CMD ["pipenv", "run", "uwsgi", "-b 8192", "--http-timeout", "300", "--harakiri", "300", "--enable-threads", "--master", "--processes", "2", "--http", "0.0.0.0:5000", "--module", "expungeservice.wsgi", "--die-on-term", "--uid", "nobody"]
