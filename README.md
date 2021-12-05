# zink

![foo](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)
![bar](https://img.shields.io/badge/code%20style-black-000000.svg)

## Settings

Moved to [settings](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).

## Basic Commands

### Setting Up Your Users

* To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

* To create an **superuser account**, use this command::

```
$ python manage.py createsuperuser
```

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### Type checks

Running type checks with mypy:

```
$ mypy zink
```

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

```
$ coverage run -m pytest
$ coverage html
$ open htmlcov/index.html
```

### Running tests with py.test

```
$ pytest
```

### Live reloading and Sass CSS compilation

Moved to [Live reloading and SASS compilation](http://cookiecutter-django.readthedocs.io/en/latest/live-reloading-and-sass-compilation.html).


## Email Server

In development, it is often nice to be able to see emails that are being sent from your application. For that reason local SMTP server `MailHog`_ with a web interface is available as docker container.

Container mailhog will start automatically when you will run all docker containers.

With MailHog running, to view messages that are sent by your application, open your browser and go to ``http://127.0.0.1:8025``

[mailhog](https://github.com/mailhog/MailHog)

## Sentry

Sentry is an error logging aggregator service. You can sign up for a free account at  https://sentry.io/signup/?code=cookiecutter  or download and host it yourself.
The system is setup with reasonable defaults, including 404 logging and integration with the WSGI application.

You must set the DSN url in production.

## Deployment

The following details how to deploy this application.

### Heroku

See detailed `cookiecutter-django Heroku documentation`_.

.. _`cookiecutter-django Heroku documentation`: http://cookiecutter-django.readthedocs.io/en/latest/deployment-on-heroku.html

### Docker

See detailed [cookiecutter-django Docker documentation](http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html).

## EXTRA

```
docker run --name zink -e POSTGRES_PASSWORD=s3cr3t -e POSTGRES_USER=zink -e POSTGRES_DB=zink -p 43210:5432 -d postgres
export USE_DOCKER=yes
export DATABASE_URL=postgres://zink:s3cr3t@localhost:43210/zink
```

## STUFF

```
docker build -t zink-web .
docker run -p 5000:5000 -e PORT=5000 -e DATABASE_URL=postgres://zink:s3cr3t@192.168.0.185:43210/zink -e DEBUG=1 --name zink-web zink-web
```

## UPDATES

Use these:
```
node update
python update
poetry update
dockerfile
```

## LOCAL

## static

localhost:8000

database:

```
docker run --name zink-db -e POSTGRES_PASSWORD=s3cr3t -e POSTGRES_USER=zink -e POSTGRES_DB=zink -p 43210:5432 -d postgres
```

web:

```
./bin/bootstrap.sh
./bin/build_theme.sh
./bin/copy_theme_to_static.sh
```

```
./manage.py collectstatic --noinput --clear
```

```
export DATABASE_URL=postgres://zink:s3cr3t@192.168.0.185:43210/zink
./manage.py runserver_plus
```

## docker

```
localhost:5000
```

database:
```
docker run --name zink-db -e POSTGRES_PASSWORD=s3cr3t -e POSTGRES_USER=zink -e POSTGRES_DB=zink -p 43210:5432 -d postgres
```

web:
```
docker build -t zink-web .
docker run -p 5000:5000 -e PORT=5000 -e DATABASE_URL=postgres://zink:s3cr3t@192.168.0.185:43210/zink -e DEBUG=1 --name zink-web zink-web
```

