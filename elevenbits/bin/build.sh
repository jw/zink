#!/usr/bin/env bash
# exit on error
set -o errexit

poetry install

bin/tailwindcss -i static/tailwind/input.css -o static/tailwind/output.css --minify

python manage.py collectstatic --no-input
python manage.py migrate
