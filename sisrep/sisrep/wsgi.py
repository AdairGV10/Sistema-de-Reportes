"""
WSGI config for sisrep project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sisrep.sisrep.settings')

# Prueba de importación
try:
    import sisrep.sisrep.settings
    print("Settings module loaded successfully!")
except ModuleNotFoundError as e:
    print(f"Error: {e}")
    sys.exit(1)

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()


