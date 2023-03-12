#!/usr/bin/env bash
set -o errexit

pip install -U pip
pip install poetry==1.4.0

poetry install

corepack enable
corepack prepare yarn@3.4.1 --activate
yarn

yarn tailwindcss -i render/static/tailwind/input.css -o render/static/tailwind/output.css --minify

python manage.py collectstatic --no-input
python manage.py migrate
