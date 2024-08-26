FROM recordsponge/expungeservice:dev
LABEL authors="Kenichi Nakamura <kenichi.nakamura@gmail.com>"

COPY backend /src/backend
RUN mkdir -p /src/backend/logs && chown nobody /src/backend/logs
RUN mkdir -p /src/backend/flask_session && chown nobody /src/backend/flask_session

COPY frontend /src/frontend

CMD ["pipenv", "run", "uwsgi", "-b 8192", "--http-timeout", "300", "--harakiri", "300", "--enable-threads", "--py-autoreload", "1", "--master", "--processes", "2", "--http", "0.0.0.0:5000", "--module", "expungeservice.wsgi", "--die-on-term", "--uid", "nobody"]
