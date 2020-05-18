FROM python:3.8-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install -U pip \
    && apt-get update \
    && apt-get install -y curl netcat \
    && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
ENV PATH="${PATH}:/root/.poetry/bin"

# postgresql
RUN apt-get install -y libpq-dev gcc

WORKDIR /app

COPY . .

RUN poetry install

RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

#RUN useradd --create-home zink
#USER zink

ENV DJANGO_SETTINGS_MODULE=elevenbits.settings
ENV PORT=8000
ENV WEB_CONCURRENCY=3

EXPOSE 8000

RUN poetry run python manage.py collectstatic --no-input --clear
# RUN poetry run python manage.py compress -v 2

CMD poetry run gunicorn elevenbits.wsgi:application --bind 0.0.0.0:$PORT

## add and run as non-root user
#RUN adduser -D myuser
#USER myuser
#
## run gunicorn
#CMD gunicorn hello_django.wsgi:application --bind 0.0.0.0:$PORT
