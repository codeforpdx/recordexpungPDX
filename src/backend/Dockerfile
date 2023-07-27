FROM python:3.9 AS base
LABEL authors="Kenichi Nakamura <kenichi.nakamura@gmail.com>"

RUN  pip install --upgrade pip && \
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

# ---

FROM base

COPY --from=build /src/venvs /src/venvs

EXPOSE 5000
CMD ["pipenv", "run", "uwsgi", "-b 8192", "--http-timeout", "300", "--harakiri", "300", "--enable-threads", "--py-autoreload", "1", "--http", "0.0.0.0:5000", "--module", "expungeservice.wsgi", "--die-on-term", "--uid", "nobody"]
