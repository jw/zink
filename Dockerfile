FROM python:3.10-buster

# install required dependencies
RUN apt-get update && apt-get install -y curl libpq-dev gcc

# node version
ENV NODE_VERSION v14.17.0
ENV NODE_DISTRO linux-x64

# install node
RUN mkdir /node && \
    cd /node && \
    curl -s -S https://nodejs.org/dist/$NODE_VERSION/node-$NODE_VERSION-$NODE_DISTRO.tar.gz -o node-$NODE_VERSION-$NODE_DISTRO.tar.gz && \
    tar xfz node-$NODE_VERSION-$NODE_DISTRO.tar.gz && \
    cd node-$NODE_VERSION-$NODE_DISTRO && \
    mv * .. && \
    cd .. && \
    rm node-$NODE_VERSION-$NODE_DISTRO.tar.gz && \
    rm -rf node-$NODE_VERSION-$NODE_DISTRO && \
    cd /
ENV PATH /node/bin:$PATH
RUN node --version

# configure Poetry
ENV POETRY_VERSION=1.2.0
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache

# install poetry separated from system interpreter
RUN python -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools \
    && $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

# Add `poetry` to PATH
ENV PATH="${PATH}:${POETRY_VENV}/bin"

# python stuff
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# zink environmemt settings
ENV DJANGO_SETTINGS_MODULE=zink.settings
ENV WEB_CONCURRENCY=3
ENV DEBUG=False

COPY . /app

# install yarn and zinks javascript dependencies and run lessc -v
RUN npm install -g yarn && yarn
ENV PATH /app/node_modules/.bin:$PATH
RUN lessc -v

# install dependencies
RUN poetry install --no-interaction --no-cache --without dev

# create statics and build search index
RUN poetry run python manage.py collectstatic --noinput --clear
# RUN poetry run python manage.py compress
# RUN poetry run python manage.py deployment

CMD [ "poetry", "run", "gunicorn", "zink.wsgi:application", "--bind 0.0.0.0:$PORT" ]
