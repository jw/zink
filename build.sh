#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -U pip
pip install poetry==1.3.2

poetry install

curl -sLO https://github.com/tailwindlabs/tailwindcss/releases/download/v3.2.7/tailwindcss-linux-x64
chmod +x tailwindcss-linux-x64
mv tailwindcss-linux-x64 tailwindcss

./tailwindcss -i render/static/tailwind/input.css -o render/static/tailwind/output.css --minify

python manage.py collectstatic --no-input
python manage.py migrate
