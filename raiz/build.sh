#!/usr/bin/env bash
# Exit on error
set -o errexit

#!/bin/bash

# Si estás en el directorio raiz/ (donde está build.sh y requirements.txt)
# Primero, instala las dependencias desde el archivo requirements.txt
pip install -r requirements.txt


# Ejecuta los comandos de Django
python manage.py collectstatic --noinput
python manage.py migrate
