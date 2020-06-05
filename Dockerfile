FROM python:3.8-slim

ENV NODE_VERSION v12.18.0
ENV NODE_DISTRO linux-x64

# install jsvascript
RUN mkdir /node && \
    cd /node && \
    apt-get update && \
    apt-get install -y curl wget && \
    curl https://nodejs.org/dist/$NODE_VERSION/node-$NODE_VERSION-$NODE_DISTRO.tar.gz -o node-$NODE_VERSION-$NODE_DISTRO.tar.gz && \
    tar xfz node-$NODE_VERSION-$NODE_DISTRO.tar.gz && \
    cd node-$NODE_VERSION-$NODE_DISTRO && \
    mv * .. && \
    cd .. && \
    cd /
ENV PATH /node/bin:$PATH

RUN node -v

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
ENV WEB_CONCURRENCY=3

RUN poetry run python manage.py collectstatic --no-input --clear
# RUN poetry run python manage.py compress -v 2

# install yarn and javascript dependencies
RUN npm install -g yarn && \
    yarn

ENV PATH /app/node_modules/.bin:$PATH
RUN echo path $PATH

RUN lessc -v

## add and run as non-root user
#RUN adduser -D myuser
#USER myuser
#
## run gunicorn
#CMD gunicorn hello_django.wsgi:application --bind 0.0.0.0:$PORT

CMD poetry run gunicorn elevenbits.wsgi:application --bind 0.0.0.0:$PORT

