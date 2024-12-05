#!/usr/bin/env bash
# Exit on error
set -o errexit

#!/bin/bash
cd ../   # Cambia al directorio raíz del proyecto, fuera de 'sisrep/'
pip install -r requirements.txt
cd sisrep  # Regresa a sisrep para ejecutar los siguientes comandos
python manage.py collectstatic --noinput
python manage.py migrate