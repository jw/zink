FROM python:3.11 as requirements-stage

WORKDIR /tmp

RUN python -m pip install -U pip poetry==1.7.1

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry self add poetry-plugin-export
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM nikolaik/python-nodejs:python3.11-nodejs20-bullseye
WORKDIR /code
COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY . .

RUN corepack enable
RUN corepack prepare yarn@4.0.2 --activate
RUN yarn
RUN yarn tailwindcss -i core/static/tailwind/input.css -o core/static/tailwind/output.css --minify

CMD ["uvicorn", "elevenbits.asgi:application", "--lifespan", "off", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]
