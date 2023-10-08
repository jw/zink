FROM python:3.11 as requirements-stage
WORKDIR /tmp
RUN pip install poetry==1.6.1
COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes


FROM nikolaik/python-nodejs:python3.11-nodejs20-bullseye
WORKDIR /code
COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY . .

RUN corepack enable
RUN corepack prepare yarn@3.4.1 --activate
RUN yarn
RUN yarn tailwindcss -i render/static/tailwind/input.css -o render/static/tailwind/output.css --minify

CMD ["uvicorn", "elevenbits.asgi:application", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]
