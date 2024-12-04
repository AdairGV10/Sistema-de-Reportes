#!/usr/bin/env bash

set -o errexit

pip install -r sisrep/requirements.txt

python manage.py collecstatic --noinput
python manage.py migrate