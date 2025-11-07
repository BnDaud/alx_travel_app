"""
WSGI config for alx_travel_app project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

# ✅ Set the Django settings module first
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_travel_app.settings')

# ✅ Then import Django's WSGI handler
from django.core.wsgi import get_wsgi_application

# ✅ Now you can import your populate script
#import populate  # temporary, runs once on app startup

# WSGI application
application = get_wsgi_application()
