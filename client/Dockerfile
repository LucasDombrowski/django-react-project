FROM node:22.14.0-bookworm-slim AS dev

ARG UID=1000
RUN userdel node && useradd django-bridge-project --uid ${UID} -l --create-home && mkdir /client && chown django-bridge-project /client

WORKDIR /client
USER django-bridge-project
