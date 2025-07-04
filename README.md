# Django Bridge app

This template provides a minimal set up to get a React and Django project running.

## Fast setup

The root folder contains a docker-compose.yml file and Makefile containing some shortcuts for docker compose.

To create the Docker environment, run `make setup`. Once that's finished, run `make start` to boot it up.

Your new Django Bridge project should be running on `localhost:8000`!

## Running it without Docker

The React code is built and served by Vite, so you need to run this alongside Django.

To run Django, run the following commands:

```
cd server
poetry install
poetry run python manage.py migrate
poetry run python manage.py runserver
```

To run the Vite server, run the following commands:

```
cd client
npm install
npm run dev
```

Django is configured (using the `DJANGO_BRIDGE['VITE_DEVSERVER_URL']` setting) to make Django Bridge fetch frontend code from the Vite devserver.

In production, you should build the frontend code with `npm run build` and set the `DJANGO_BRIDGE['VITE_BUNDLE_DIR']` to the location of the folder that contains `.vite` and `assets` folders that Vite created.
