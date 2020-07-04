FROM python:3.8-buster

# install required dependencies
# todo: cleanup necessary
RUN apt-get update \
    && apt-get install -y curl libpq-dev gcc tree

# install latest poetry
RUN pip install -U pip \
    && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
ENV PATH="${PATH}:/root/.poetry/bin"
RUN poetry --version
RUN poetry config --list

# python stuff
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# zink environmemt settings
ENV DJANGO_SETTINGS_MODULE=zink.settings
ENV WEB_CONCURRENCY=3
ENV DEBUG=0

COPY . .

# install dependencies
RUN POETRY_VIRTUALENVS_CREATE=false poetry install --no-interaction

CMD gunicorn zink.wsgi:application --bind 0.0.0.0:$PORT