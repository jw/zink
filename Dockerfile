FROM python:3.11 as requirements-stage
WORKDIR /tmp
RUN pip install poetry==1.6.1
COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.11
WORKDIR /code
COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY . .

CMD ["uvicorn", "elevenbits.asgi:application", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]
