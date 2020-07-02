FROM python:3.8-buster

# install required dependencies
RUN apt-get update && \
    apt-get install -y curl libpq-dev gcc tree

# node version
ENV NODE_VERSION v12.18.0
ENV NODE_DISTRO linux-x64

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
RUN node --version

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

# install yarn and zinks javascript dependencies and run lessc
RUN npm install -g yarn && yarn
ENV PATH /app/node_modules/.bin:$PATH
RUN lessc -v

# install dependencies
RUN POETRY_VIRTUALENVS_CREATE=false poetry install --no-interaction

#RUN python manage.py collectstatic --no-input --clear
#RUN python manage.py compress --force -v 2

# at last, start it!
#CMD gunicorn elevenbits.wsgi:application --bind 0.0.0.0:$PORT
