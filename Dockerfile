FROM node:20-bookworm-slim AS assets

WORKDIR /code
COPY . .

RUN corepack enable && corepack prepare yarn@4.0.2 --activate
RUN yarn install --immutable
RUN yarn build:canvas-css

FROM python:3.14.2 AS pydeps

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
WORKDIR /code

COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-install-project

COPY . .
RUN uv sync --locked

FROM python:3.14.2-slim

WORKDIR /code
COPY --from=pydeps /code /code
COPY --from=assets /code/core/static/css/style.css /code/core/static/css/style-rtl.css core/static/css/

ENV PATH="/code/.venv/bin:$PATH"

CMD ["sh", "-c", "python manage.py collectstatic --no-input && python manage.py migrate --no-input && python manage.py loaddata blog && exec uvicorn elevenbits.asgi:application --lifespan off --proxy-headers --host 0.0.0.0 --port 80"]
