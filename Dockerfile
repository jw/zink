FROM python:3.8-slim

# node version
ENV NODE_VERSION v12.18.0
ENV NODE_DISTRO linux-x64

# python stuff
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install required dependencies
RUN apt-get update && \
    apt-get install -y curl libpq-dev gcc

# install node
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
# some magic for heroku
RUN mkdir -p ${HOME}/.config/pypoetry/ && \
    touch ${HOME}/.config/pypoetry/config.toml && \
    poetry config virtualenvs.create false

# build zink
WORKDIR /app
COPY . .
RUN poetry install
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

# zink environmemt settings
ENV DJANGO_SETTINGS_MODULE=elevenbits.settings
ENV WEB_CONCURRENCY=3

# create statics
RUN env
RUN poetry run python manage.py collectstatic --noinput -v 2

# install yarn and zinks javascript dependencies and run lessc
RUN npm install -g yarn && yarn
ENV PATH /app/node_modules/.bin:$PATH
RUN lessc -v
RUN poetry run python manage.py compress -v 2

# at last, start it!
CMD poetry run gunicorn zink.wsgi:application --bind 0.0.0.0:$PORT
