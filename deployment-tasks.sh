#!/usr/bin/env bash
echo $PYTHONPATH
echo $PATH
env

poetry -V
poetry --local --list
poetry --list
poetry env info

poetry run python manage.py collectstatic --no-input --clear
poetry run python manage.py compress -v 2
