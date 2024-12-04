"""
WSGI config for sisrep project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

# Depuración: Mostrar las rutas de búsqueda de módulos
print("Rutas de búsqueda de módulos:")
print(sys.path)

# Añadir la ruta del proyecto al sys.path para asegurarnos de que 'core' sea accesible
sys.path.append(os.path.join(os.path.dirname(__file__), 'sisrep'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sisrep.sisrep.settings')

application = get_wsgi_application()

