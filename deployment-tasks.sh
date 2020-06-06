#!/usr/bin/env bash
echo $PYTHONPATH
echo $PATH
env

poetry -V
poetry config --local --list
poetry config --list

poetry env info

python -V
which python

ls -al `poetry config virtualenvs.path`

poetry run python manage.py collectstatic --no-input --clear
poetry run python manage.py compress -v 2
