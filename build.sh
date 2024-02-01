#!/usr/bin/env bash
set -o errexit

python -m pip install -U pip
python -m pip install pipx
python -m pipx install poetry

poetry install --no-root

corepack enable
corepack prepare yarn@stable --activate
yarn set version stable
yarn

yarn tailwindcss -i core/static/tailwind/input.css -o core/static/tailwind/output.css --minify

python manage.py collectstatic --no-input
python manage.py migrate
python manage.py loaddata blog
