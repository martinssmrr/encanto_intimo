"""
WSGI config for encanto_intimo project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Para produção, certifique-se de que a variável de ambiente 
# DJANGO_SETTINGS_MODULE está definida como 'encanto_intimo.settings.prod'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "encanto_intimo.settings.prod")

application = get_wsgi_application()
