"""
WSGI config for sisrep project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sisrep.sisrep.settings')

# Intentar importar core
try:
    import core
except ModuleNotFoundError as e:
    print(f"Error al importar 'core': {e}")
    sys.exit(1)

application = get_wsgi_application()
