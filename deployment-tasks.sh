#!/usr/bin/env bash
poetry run python manage.py collectstatic --no-input --clear
poetry run python manage.py compress -v 2
