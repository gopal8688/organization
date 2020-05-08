"""
WSGI config for base project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os, sys

# add the base project path into the sys.path
sys.path.append('/var/www/html/customer/customer')

# add the virtualenv site-packages path to the sys.path
sys.path.append('/usr/local/lib/python3.6/dist-packages')

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'customer.settings.development')

application = get_wsgi_application()
