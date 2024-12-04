#!/usr/bin/env bash

set -o errexit

pip install -r sisrep/requirements.txt

python sisrep/manage.py collecstatic --noinput
python sisrep/manage.py migrate