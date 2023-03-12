#!/usr/bin/env bash
set -o errexit

pip install -U pip
pip install poetry==1.4.0

poetry install

yarn add -D tailwind
yarn add -D daisyui
yarn add -D @tailwindcss/typography

yarn tailwindcss -i render/static/tailwind/input.css -o render/static/tailwind/output.css --minify

python manage.py collectstatic --no-input
python manage.py migrate
