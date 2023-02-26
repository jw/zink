#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -U pip
pip install poetry==1.3.2

poetry install

python manage.py collectstatic --no-input
python manage.py migrate
