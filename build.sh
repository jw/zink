#!/usr/bin/env bash
# exit on error
set -o errexit

poetry install

./bin/tailwindcss -i input.css -o output.css --minify
python manage.py collectstatic --no-input
python manage.py migrate
