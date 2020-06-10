#!/usr/bin/env bash
yarn install --verbose
python manage.py collectstatic --no-input --clear
python manage.py compress --force -v 2
