FROM python:3.8-slim

ENV NODE_VERSION v12.18.0
ENV NODE_DISTRO linux-x64

# python stuff
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install required dependencies and tools
RUN apt-get update && \
    apt-get install -y curl wget netcat libpq-dev gcc

# install node (and cleanup the tar.gz)
RUN mkdir /node && \
    cd /node && \
    curl https://nodejs.org/dist/$NODE_VERSION/node-$NODE_VERSION-$NODE_DISTRO.tar.gz -o node-$NODE_VERSION-$NODE_DISTRO.tar.gz && \
    tar xfz node-$NODE_VERSION-$NODE_DISTRO.tar.gz && \
    cd node-$NODE_VERSION-$NODE_DISTRO && \
    mv * .. && \
    cd .. && \
    rm node-$NODE_VERSION-$NODE_DISTRO.tar.gz && \
    rm -rf node-$NODE_VERSION-$NODE_DISTRO && \
    cd /
ENV PATH /node/bin:$PATH

# install latest poetry
RUN pip install -U pip \
    && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
ENV PATH="${PATH}:/root/.poetry/bin"
RUN mkdir -p ${HOME}/.config/pypoetry/ && \
    touch ${HOME}/.config/pypoetry/config.toml && \
    poetry config virtualenvs.create false  # some magic for heroku

# build zink
WORKDIR /app
COPY . .
RUN poetry install && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

ENV DJANGO_SETTINGS_MODULE=elevenbits.settings
ENV WEB_CONCURRENCY=3

# install yarn and zinks javascript dependencies
RUN npm install -g yarn && yarn
ENV PATH /app/node_modules/.bin:$PATH

#RUN useradd --create-home zink
#USER zink

#RUN poetry run python manage.py collectstatic --no-input --clear
#RUN poetry run python manage.py compress -v 2
#CMD gunicorn hello_django.wsgi:application --bind 0.0.0.0:$PORT

#RUN adduser -D myuser
#USER myuser

CMD poetry run gunicorn elevenbits.wsgi:application --bind 0.0.0.0:$PORT

