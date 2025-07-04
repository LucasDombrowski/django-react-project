FROM node:22.14.0-bookworm-slim AS client

# Install client dependencies
COPY client/package.json client/package-lock.json /client/
RUN cd /client && npm install

# Copy the source code of the client into the container.
COPY client /client

# Build the client
RUN cd /client && npm run build

FROM python:3.13.2-slim-bookworm AS base

RUN apt update -y \
    && apt install -y --no-install-recommends \
    # Required to build psycopg2
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

ENV VIRTUAL_ENV=/venv
ENV PATH=$VIRTUAL_ENV/bin:$PATH \
    PYTHONPATH=/app \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=django_bridge_project.settings \
    PORT=8000

# Add user that will be used in the container
ARG UID=1000
RUN useradd django-bridge-project --uid ${UID} --create-home && mkdir /app $VIRTUAL_ENV && chown -R django-bridge-project /app $VIRTUAL_ENV

# Install poetry
RUN pip install poetry==2.1.1

# Use user "django-bridge-project" to run the build commands below and the server itself.
USER django-bridge-project

# Use /app folder as a directory where the source code is stored.
WORKDIR /app

# Set up virtual environment
RUN python -m venv $VIRTUAL_ENV

# Install Python dependencies
COPY --chown=django-bridge-project server/pyproject.toml server/poetry.lock ./
RUN poetry install --no-root --only main

# Copy the source code of the project into the container.
COPY --chown=django-bridge-project server .

# Run poetry install again to install our project
RUN poetry install --only main

FROM base AS prod

# Copy the client bundle from the client target
COPY --chown=django-bridge-project --from=client /client/dist /client

# Collect static files
ENV VITE_BUNDLE_DIR=/client
RUN DJANGO_SECRET_KEY=secret python manage.py collectstatic --noinput --clear

CMD gunicorn -w 4 --threads 2 django_bridge_project.wsgi:application

FROM base AS dev

# Install dev dependencies
RUN poetry install
